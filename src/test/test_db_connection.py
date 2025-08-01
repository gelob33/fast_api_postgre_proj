import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.exc import ProgrammingError
from src.database.connection import get_conn
from src.common.exceptions import DatabaseConnectionError

@pytest.mark.asyncio
async def test_get_conn_unexpected_exception():
    # Patch get_engine().connect() to raise a generic Exception
    with patch("src.database.connection.get_engine") as mock_get_engine:
        mock_engine = AsyncMock()
        mock_engine.connect.side_effect = Exception("Shalalalala!")
        mock_get_engine.return_value = mock_engine

        # Run and assert
        with pytest.raises(DatabaseConnectionError) as exc_info:
            async with get_conn():
                pass  # Should never reach here

        # Assert exception message
        assert "Unexpected database error" in str(exc_info.value)

        # Assert original exception is preserved
        assert isinstance(exc_info.value.__cause__, Exception)
        assert str(exc_info.value.__cause__) == "Shalalalala!"

@pytest.mark.asyncio
async def test_invalid_sql_syntax():
    # Patch get_engine().connect() to return a mock connection
    with patch("src.database.connection.get_engine") as mock_get_engine:
        mock_conn = AsyncMock()
        mock_conn.execute.side_effect = ProgrammingError("SELECT * FORM bart", {}, None)  # typo: FORM and invalid table name
        mock_engine = AsyncMock()
        mock_engine.connect.return_value = mock_conn
        mock_get_engine.return_value = mock_engine

        # Run and assert
        with pytest.raises(DatabaseConnectionError) as exc_info:
            async with get_conn() as conn:
                await conn.execute("SELECT * FORM bart")  # typo: FORM and invalid table name

        # Assert exception message
        assert "Database connection failed" in str(exc_info.value)

        # Assert original exception is preserved
        assert isinstance(exc_info.value.__cause__, ProgrammingError)


