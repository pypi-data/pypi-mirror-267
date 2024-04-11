import pickle  # noqa
import warnings

from pathlib import Path
from typing import List, Literal, Union

import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import quantstats as qt
from kneed import KneeLocator
from sklearn.cluster import Birch, KMeans
from sklearn.metrics import silhouette_score
from sktime.clustering.k_means import TimeSeriesKMeansTslearn 

from .classes import PIP, SeqKMeans

warnings.filterwarnings("ignore", category=RuntimeWarning)


class Miner:
    def __init__(self, 
                 n_lookback: int, 
                 n_pivots: int, 
                 n_clusters: int = 8,
                 hold_period: int = 6,
                 model_type:Literal['standard', 'ts', 'sequential']='standard') -> None:
        self.n_lookback = n_lookback
        self.n_pivots = n_pivots
        self.hold_period = hold_period
        self.n_cluster = n_clusters

        self._model_type = model_type

        # Store Training Data
        self._data: List = []
        self._data_train_X: Union[List, np.ndarray] = []
        self._data_train_y: Union[List, np.ndarray] = []

        # Store Clusters Assignments
        self._unique_pip_indices : Union[List, np.ndarray]= []
        self._cluster_labels = []

        # Store Selected Cluster Labels
        self._cluster_labels_long = []
        self._cluster_labels_short = []

        # Store the dimensionality reduction agent
        self._agent_reduce: PIP = None

        # Store the clustering agent
        self._agent_cluster = None

        # Preset attributes
        
        self._random_state = 0


    def fit(self, data: np.ndarray):
        # Set the random state
        np.random.seed(self._random_state)

        # Preprocess the training data
        self._preprocess_data(data)

        # Create training dataset
        self._generate_training_set()

        # Transform the training data for clustering
        self._transform_data()

        # Cluster the data
        self._generate_clusters()

        # Assign Training Data to cluster
        self._assign_cluster_labels() 

        # Assess Each Clusters Performance
        # Performance metric : Martin's Ratio
        # Evaluation metric : Hold Period
        self._assess_clusters()

        # Test the performance of the selected clusters
        martins = self._compute_performance()

        print("Training Complete : ", martins)

        # Clean up stored data
        self._cleanup()


    def test(self, data: List[np.ndarray], plot_equity=False):
        # Preprocess Data
        data = self._preprocess_data(data, test_mode=True)
        _returns = np.diff(data, prepend=data[0])

        # Generate data windows
        windows = self._generate_training_set(data)

        # Transform the Data
        _pivots, _unique_indices = self._transform_data(windows)

        # Generate the cluster labels
        _l = self._agent_cluster.predict(_pivots)
        indices = _unique_indices + self.n_lookback - 1
        _labels = self._assign_cluster_labels(data, _l, indices)

        # Filter for only selected labels
        mask_long = np.isin(_labels, self._cluster_labels_long)
        mask_short = np.isin(_labels, self._cluster_labels_short)

        # Generate the signals
        _signals = np.zeros_like(_returns)
        _signals[mask_long] = 1
        _signals[mask_short] = -1

        # Implement holding period
        _signals = self.__apply_holding_period(_signals)

        # Get the returns, compute martin score
        _returns = _signals * _returns

        print("Test Martin Score : ", self.__compute_martin(_returns))

        if plot_equity:
            plt.plot(np.cumsum(_returns))
            plt.show()

        ser = pd.Series(_returns)

        print("Profit Factor : ", qt.stats.profit_factor(ser))
        print("Risk of Ruin : ", qt.stats.risk_of_ruin(ser))
        print("Sharpe : ", qt.stats.sharpe(ser))
        print("Avg Win : ", qt.stats.avg_win(ser))
        print("Avg Loss : ", qt.stats.avg_loss(ser))
        print("Avg Return : ", qt.stats.avg_return(ser))


    def transform(self, data:Union[List, np.ndarray]):
        """
        Generate labels for a full dataset.
        """
        # Preprocess Data
        data = self._preprocess_data(data, test_mode=True)

        # Generate data windows
        windows = self._generate_training_set(data)

        # Transform the Data
        _pivots, _unique_indices = self._transform_data(windows)

        # Generate the cluster labels
        _l = self._agent_cluster.predict(_pivots)
        indices = _unique_indices + self.n_lookback - 1
        _labels = self._assign_cluster_labels(data, _l, indices)

        return _labels
        

    def generate_signal(self, data: List[np.ndarray]):
        """
        This generates signal for one data window.

        Return:
            signal, pivots : Tuple containing the predicted signal, and the list of pivots points.
        """
        data = np.atleast_2d(self._preprocess_data(data, test_mode=True))

        # Generate entry signals from a data window
        _pivots = self._agent_reduce.transform(data)

        pivots = self.__normalizer_standard(_pivots)
        _l = self._agent_cluster.predict(pivots)

        signal = (
            1
            if _l in self._cluster_labels_long
            else -1
            if _l in self._cluster_labels_short
            else 0
        )

        return signal, list(np.squeeze(_pivots))


    def save_model(self, path:Union[Path, str]):
        # Convert path to Path object, and check if it exists
        if not isinstance(path, Path):
            path = Path(str)
            
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            
        # Save model
        with open(path, 'wb') as f:
            try:
                pickle.dump(self, f)
                print(f'Model saved at {path}')
            except Exception as e:
                raise e
    
    @staticmethod
    def load_model(path:Union[Path, str]):
        # Convert path to Path object, and check if it exists
        if not isinstance(path, Path):
            path = Path(str)
            
            if not path.exists():
                raise FileNotFoundError(f"File not found. Model does not exist at : {path}")
            
        # Save model
        with open(path, 'rb') as f:
            try:
                miner = pickle.load(f)
                print(f'Model Loaded from : {path}')
            except Exception as e:
                raise e
        
        return miner 


    def _preprocess_data(self, data, **kwargs):
        """
        Perform series-level data transformations. These can include detrending, denoising/filtering, domain transformations.
        The parameters of these transformations are saved, to be used for new data.
        """

        if kwargs.get("test_mode", False):
            return np.log(data)

        self._data = np.log(data)


    def _generate_training_set(self, data: np.ndarray = None):
        """
        Generate the trainging input (X) and target (y) datasets. When running a test, the `data` parameter is to be processed.
        """
        # Clear stores for training data
        self._data_train_X.clear()
        self._data_train_y.clear()

        # Initialize variables
        test_mode = data is not None # if data is passed, test_mode is active
        lookback = self.n_lookback
        windows = []
    
        if not test_mode:
            data = self._data

        # Assert there is data
        assert (
            len(data) > 0
        ), "One of the passed raw data does not contain sufficient data."

        if not isinstance(data, np.ndarray):
            data = np.array(data)

        # Iterate through the data and append the data windows
        for index in range(lookback, len(data)):
            try:
                start_index = index - lookback
                end_index = index

                windows.append(data[start_index:end_index])

            except Exception as e:
                print("Error Occured : \n", e)
                continue

        # During tests, return the generated data windows
        if test_mode:
            return np.array(windows)

        # For training, assign windows to training data
        self._data_train_X = np.array(windows)


    def _transform_data(self, data: np.ndarray = None):
        """
        Transform the generated training set data for clustering. If data is passed, transform the data passed only.
        Transformations include scaling/normalization, dimensionality reduction, etc.

        Return:
            data [np.ndarray] : Numpy array containing clustering-ready data.
        """

        test_mode = data is not None
        
        if not test_mode:
            data = self._data_train_X
        
        # Ensure the training set has been generated
        if len(data) < 0:
            raise ValueError("No training data to transform")

        # Dimensionality Reduction
        if (self._agent_reduce is None):
            if not test_mode:
                self._agent_reduce = PIP(n_pivots=self.n_pivots, dist_measure=1)
            
            else:
                raise ValueError("Model has not been training. self._agent_reduce is missing.")

        pivots = self._agent_reduce.transform(data)

        # Only keep unique patterns
        null_pivots = [-1] * self.n_pivots

        # Compare each group with the previous one, excluding the first and last items
        is_duplicate = np.all(pivots[1:, 1:-1] == pivots[:-1, 1:-1], axis=1)

        # Replace duplicates with null_pivots
        pivots[1:][is_duplicate] = null_pivots

        # Remove null_pivots
        mask_unique = np.all(pivots != null_pivots, axis=1)
        pivots = pivots[mask_unique]

        # Data Scaling / Normalization ; Element-wise for each individual window
        data = np.apply_along_axis(
            self.__normalizer_standard, axis=1, arr=pivots
        )

        # For test mode
        if test_mode:
            return data, np.where(mask_unique)[0]

        # Get the indices where value is True
        self._data_train_X = data
        self._unique_pip_indices = np.where(mask_unique)[0]


    def _generate_clusters(self):
        """
        Cluster the training data. Default n_clusters
        """
        
        # self.n_cluster = self.__find_n_clusters()
        
        # SKTime (TSLearn) Kmeans
        if self._model_type == 'ts':
            self._agent_cluster = TimeSeriesKMeansTslearn(n_clusters=self.n_cluster,
                                    metric='euclidean',
                                    n_jobs=-1,
                                    random_state=self._random_state,
                                    )

        elif self._model_type == 'standard':
            self._agent_cluster = KMeans(
                n_clusters=self.n_cluster,
                n_init="auto",
                random_state=self._random_state,
                )

        elif self._model_type == "sequential":
            self._agent_cluster = SeqKMeans(
                n_clusters=self.n_cluster, 
                learning_rate=0.5, 
                centroid_update_threshold_std=3, 
                verbose=False,
                fit_method='sequential',
                random_state=self._random_state,
                )

        print("Clustering data...")

        self._agent_cluster.fit(self._data_train_X)

        print("Clustering complete")


    def _assign_cluster_labels(
        self,
        data: np.ndarray = None,
        _labels: np.ndarray = None,
        indices: np.ndarray = None,
    ):
        """
        Assign clusters labels to each data point in the data.
        """
        self._cluster_labels.clear()
        test_mode = data is not None

        if data is None:
            # Get raw data
            data = self._data

            # Get the labels from agent_cluster
            _labels = self._agent_cluster.labels_

            # Get the unique pips indices
            indices = self._unique_pip_indices + self.n_lookback - 1

        assert _labels is not None, "`_labels` array cannot be None."
        assert indices is not None, "`indices` array cannot be None."

        # Assign placeholder signals
        labels = np.ones(len(data)) * -1
        labels[indices] = _labels

        # For tests, return the labels
        if test_mode:
            return np.array(labels)

        self._cluster_labels = np.array(labels)
    

    def _assess_clusters(self):
        """
        Assess each cluster's performance, and selected the best performing clusters
        """
        self._cluster_labels_long.clear()
        self._cluster_labels_short.clear()

        # Store the cluster scores from each data
        cluster_scores = []

        # Compute the returns
        _returns = np.diff(self._data, prepend=self._data[0])

        # Get the cluster labels
        _labels = self._cluster_labels

        # Iterate through each cluster label
        for _label in range(self.n_cluster):
            # Create a mask for the label in the labels; everything else should be zero
            mask_label: np.ndarray = _labels == _label

            # Filter the labels
            _signals = mask_label.astype(int)

            # Implement Holding Period
            _signals = self.__apply_holding_period(_signals)

            # Get the returns, compute martin score
            _ret = _signals * _returns
            cluster_scores.append(self.__compute_martin(_ret))

        # Append the selected cluster labels
        self._cluster_labels_long.append(np.argmax(cluster_scores))
        self._cluster_labels_short.append(np.argmin(cluster_scores))


    def _compute_performance(self):
        """
        Test the performance of the selected clusters
        """

        _returns = np.diff(self._data, prepend=self._data[0])

        # Get the full labels
        _labels = self._cluster_labels

        # Filter for only selected labels
        mask_long = np.isin(_labels, self._cluster_labels_long)
        mask_short = np.isin(_labels, self._cluster_labels_short)

        # Generate the signals
        _signals = np.zeros_like(_returns)
        _signals[mask_long] = 1
        _signals[mask_short] = -1

        # Implement the holding period
        _signals = self.__apply_holding_period(_signals)

        # Get the returns, compute martin score
        _returns = _signals * _returns

        return self.__compute_martin(_returns)


    def _cleanup(self):
        """
        Clear up memory used to store training data
        """

        # Clear Training Data
        self._data = []
        self._data_train_X = []
        self._data_train_y = []

        # Clear Clusters Assignments
        self._unique_pip_indices = []
        self._cluster_labels = []


    def __apply_holding_period(self, signals):
        """Apply holding period logic to signals."""
        prev = 0

        for index, signal in enumerate(signals):
            if (signal != 0) and (index > (prev + self.hold_period)):
                prev = index
                end_index = min(index + self.hold_period + 1, len(signals))
                signals[index + 1 : end_index] = signal
                signals[index] = 0
        return signals


    def __compute_martin(self, rets: np.array):
    
        rsum = np.sum(rets)
        short = False
        if rsum < 0.0:
            rets *= -1
            rsum *= -1
            short = True

        csum = np.cumsum(rets)
        eq = pd.Series(np.exp(csum))
        sumsq = np.sum(((eq / eq.cummax()) - 1) ** 2.0)
        ulcer_index = (sumsq / len(rets)) ** 0.5
        martin = rsum / (ulcer_index + 1.0e-10)
        if short:
            martin = -martin

        return martin


    def __find_n_clusters(self):
        # Assuming X is your time series data
        n_clusters = range(2, 50)  # change this range according to your needs
        silhouette_scores = []
        X = self._data_train_X

        # Get the silhouette scores
        for n in n_clusters:
            birch = Birch(n_clusters=n)
            kmeans = KMeans(n_clusters=n, n_init="auto")

            birch.fit(X)
            kmeans.fit(X)

            silhouette_scores.append(
                np.mean(
                    [
                        silhouette_score(X, birch.labels_),
                        silhouette_score(X, kmeans.labels_),
                    ]
                )
            )

        kneedle = KneeLocator(
            range(2, 50),
            np.array(silhouette_scores),
            S=1.0,
            curve="convex",
            direction="decreasing",
        )
        optimal_n = kneedle.knee

        print("Optimal N: ", optimal_n)

        return optimal_n


    def __normalizer_standard(self, points):
        points = np.array(points)

        points = (points - np.mean(points)) / (np.std(points) + 1e-10)
        return np.array(points)


    def __visualize_clusters(self, data, labels):
        import plotly.graph_objects as go

        # Create a subplot for the time series data
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=data, mode="lines", name="Data"))

        # Create a subplot for the labels
        fig.add_trace(go.Scatter(y=labels, mode="lines", name="Labels"))

        # Enable spike lines
        fig.update_layout(
            hovermode="x",
            spikedistance=-1,
            xaxis=dict(
                showspikes=True,
                spikemode="across",
                spikesnap="cursor",
                spikedash="solid",
            ),
            yaxis=dict(
                showspikes=True,
                spikemode="across",
                spikesnap="cursor",
                spikedash="solid",
            ),
        )

        # Show the plot
        fig.show()


if __name__ == "__main__":
    parent_path = Path(__file__).parent
    btc_path = parent_path / 'data/BTCUSDT_FULL.parquet'
    
    # Define your date range
    start_date = "2017-12-01"
    end_date = "2022-12-31"

    raw_data = pd.read_parquet(btc_path)

    # Filter the DataFrame
    train_data = raw_data[(raw_data.index >= start_date) & (raw_data.index <= end_date)]
    test_data = raw_data[
        (raw_data.index >= "2023-01-01") & (raw_data.index <= "2023-12-31")
    ]

    train_data = train_data["close"].dropna(axis=0)
    train_data = train_data.to_numpy()

    test_data = test_data["close"].dropna(axis=0)
    test_data = test_data.to_numpy()

    # miner = Miner(25, 5)
    # miner.fit(train_data)

    # miner.save_model(parent_path / 'pipminer.pkl')

    miner : Miner = Miner.load_model(parent_path / 'pipminer.pkl')

    print(miner.transform(test_data))

    # miner.test(test_data)
    print('Successful')
