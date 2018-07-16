from phytebyte import PhyteByte
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_probability():
    return 100.00


@pytest.fixture
def mock_negative_sampler():
    mock_neg_sampler = Mock()
    return mock_neg_sampler


@pytest.fixture
def mock_positive_clusterer():
    mock_pos_clusterer = Mock()
    return mock_pos_clusterer


@pytest.fixture
def mock_target_input():
    mock_target_input = Mock()
    return mock_target_input


@pytest.fixture
def mock_source():
    mock_source = Mock()
    return mock_source


@pytest.fixture
def mock_binary_classifier_model():
    bcm = Mock()
    bcm.expected_encoding = 'numpy'
    bcm.train = MagicMock(return_value=None)
    return bcm


@pytest.fixture
def mock_binary_classifier_input():
    return Mock()


@pytest.fixture
def mock_ModelInputLoader(mock_binary_classifier_input):
    class ModelInputLoaderMock():
        load_calls = []

        def __init__(self, *args, **kwargs):
            pass

        def load(self, *args, **kwargs):
            self.load_calls.append(args)
            return mock_binary_classifier_input

    return ModelInputLoaderMock


@pytest.fixture
def mock_fingerprinter():
    fp = Mock()
    fp.fingerprint_and_encode = MagicMock(return_value=Mock())
    return fp


@pytest.fixture
def mock_food_cmpd_iterator():
    return (Mock() for _ in range(10))


@pytest.fixture
def mock_food_cmpd_source(mock_food_cmpd_iterator):
    m = Mock()
    m.fetch_all_cmpds = MagicMock(return_value=mock_food_cmpd_iterator)
    return m


@pytest.fixture
def phytebyte_fixture(monkeypatch,
                      mock_positive_clusterer,
                      mock_negative_sampler,
                      mock_source,
                      mock_target_input,
                      mock_binary_classifier_model,
                      mock_binary_classifier_input,
                      mock_fingerprinter,
                      mock_ModelInputLoader):
    monkeypatch.setattr("phytebyte.phytebyte.ModelInputLoader",
                        mock_ModelInputLoader)
    # Mock BinaryClassifierModel.create factory method
    mock_base_binary_classifier_model = Mock()
    mock_base_binary_classifier_model.create = MagicMock(
        return_value=mock_binary_classifier_model)
    monkeypatch.setattr("phytebyte.phytebyte.BinaryClassifierModel",
                        mock_base_binary_classifier_model)
    # Mock Clusterer.create factory method
    mock_base_pos_clusterer = Mock()
    mock_base_pos_clusterer.create = MagicMock(
        return_value=mock_positive_clusterer)
    monkeypatch.setattr("phytebyte.phytebyte.Clusterer",
                        mock_base_pos_clusterer)
    # Mock NegativeSampler.create factory method
    mock_base_neg_sampler = Mock()
    mock_base_neg_sampler.create = MagicMock(
         return_value=mock_negative_sampler)
    monkeypatch.setattr("phytebyte.phytebyte.NegativeSampler",
                        mock_base_neg_sampler)
    # Mock Fingerprinter.create factory method
    mock_base_fingerprinter = Mock()
    mock_base_fingerprinter.create = MagicMock(
        return_value=mock_fingerprinter)
    monkeypatch.setattr("phytebyte.phytebyte.Fingerprinter",
                        mock_base_fingerprinter)
    # Builder pattern
    pb = PhyteByte()
    # Factory method proxies
    pb.set_positive_clusterer("Whocares")
    pb.set_negative_sampler("Not me!")
    pb.set_fingerprinter("Doin't care!")

    pb.set_source(mock_source)
    pb.set_target_input(mock_target_input)
    return pb


@pytest.fixture
def phytebyte_fixture_with_model(phytebyte_fixture):
    phytebyte_fixture.model = Mock()
    phytebyte_fixture.model.calc_score = MagicMock(return_value=100.00)
    return phytebyte_fixture


def test_init():
    pb = PhyteByte()
    assert pb.model is None


def test_set_negative_sampler(monkeypatch, mock_negative_sampler):
    mock_base_neg_sampler = Mock()
    mock_base_neg_sampler.create = MagicMock(
         return_value=mock_negative_sampler)
    monkeypatch.setattr("phytebyte.phytebyte.NegativeSampler",
                        mock_base_neg_sampler)
    pb = PhyteByte()
    pb.set_negative_sampler("Tanimoto")
    assert pb._negative_sampler == mock_negative_sampler


def test_set_positive_clusterer(monkeypatch, mock_positive_clusterer):
    mock_base_pos_clusterer = Mock()
    mock_base_pos_clusterer.create = MagicMock(
        return_value=mock_positive_clusterer)
    monkeypatch.setattr("phytebyte.phytebyte.Clusterer",
                        mock_base_pos_clusterer)
    pb = PhyteByte()
    pb.set_positive_clusterer("Foobar!")
    assert pb._positive_clusterer == mock_positive_clusterer


def test_set_fingerprinter(monkeypatch, mock_fingerprinter):
    mock_base_fingerprinter = Mock()
    mock_base_fingerprinter.create = MagicMock(
        return_value=mock_fingerprinter)
    monkeypatch.setattr("phytebyte.phytebyte.Fingerprinter",
                        mock_base_fingerprinter)
    pb = PhyteByte()
    pb.set_fingerprinter("no one cares!!!")
    assert pb._fingerprinter == mock_fingerprinter


def test_set_target_input(mock_target_input):
    pb = PhyteByte()
    pb.set_target_input(mock_target_input)
    assert pb._target_input == mock_target_input


def test_set_source(mock_source):
    pb = PhyteByte()
    pb.set_source(mock_source)
    assert pb._source == mock_source


def test_train_model_calls__BinaryClassifierModel_train(
        mock_binary_classifier_input,
        mock_binary_classifier_model,
        phytebyte_fixture):
    phytebyte_fixture.train_model('model_type', 1000)
    mock_binary_classifier_model.train.assert_called_with(
        mock_binary_classifier_input)


def test_train_model_calls__ModelInputLoader_load(mock_ModelInputLoader,
                                                  mock_fingerprinter,
                                                  phytebyte_fixture):
    phytebyte_fixture.train_model('model_type', 1000)
    assert len(mock_ModelInputLoader.load_calls) == 1
    assert mock_ModelInputLoader.load_calls == [(1000, mock_fingerprinter,)]


def test_train_model__sets_model(phytebyte_fixture,
                                 mock_binary_classifier_model):
    phytebyte_fixture.train_model('model_type', 1000)
    assert phytebyte_fixture.model == mock_binary_classifier_model


def test_predict_bioactive_food_cmpd_iter__returns_iter(
        phytebyte_fixture_with_model,
        mock_food_cmpd_source):
    phytebyte_fixture_with_model.model.calc_score = MagicMock(
        return_value=mock_probability)
    food_cmpd_iter = phytebyte_fixture_with_model.\
        predict_bioactive_food_cmpd_iter(
            mock_food_cmpd_source)
    assert next(food_cmpd_iter) is not None


def test_predict_bioactive_food_cmpd_iter__calls_fetch_all_cmpds(
        phytebyte_fixture_with_model,
        mock_food_cmpd_source):
    phytebyte_fixture_with_model.model.calc_score = MagicMock(
        return_value=mock_probability)
    food_cmpd_iter = phytebyte_fixture_with_model.\
        predict_bioactive_food_cmpd_iter(
            mock_food_cmpd_source)
    next(food_cmpd_iter)
    mock_food_cmpd_source.fetch_all_cmpds.assert_called_once()


@pytest.mark.xfail
def test_load_config():
    PhyteByte("path_to_config")
