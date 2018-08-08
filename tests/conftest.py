import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_streaming_engine_factory():

    def create_mock_streaming_engine(mock_rows, num_chunks=1):
        chunk_size = (len(mock_rows) // num_chunks) + 1

        class MockChunkIterator():
            _num_chunks = num_chunks
            _fetchmany_calls = 0

            def fetchmany(self, _):
                if self._fetchmany_calls == self._num_chunks:
                    return None
                start = self._fetchmany_calls * chunk_size
                self._fetchmany_calls += 1
                end = self._fetchmany_calls * chunk_size
                chunk = mock_rows[start: end]
                return chunk
        # Support context-managers
        mock_conn = Mock()
        mock_conn.execute = MagicMock(return_value=MockChunkIterator())
        mock_conn.__enter__ = Mock(return_value=mock_conn)
        mock_conn.__exit__ = Mock(return_value=None)
        mock_engine = Mock()
        mock_engine.connect = MagicMock(return_value=mock_conn)
        mock_engine.execute_options = MagicMock()
        return mock_engine
    return create_mock_streaming_engine
