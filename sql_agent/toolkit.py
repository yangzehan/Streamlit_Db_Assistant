"""Toolkit for interacting with a SQL database."""
from typing import List

from pydantic import Field

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.schema.language_model import BaseLanguageModel
from langchain.sql_database import SQLDatabase
from langchain.tools import BaseTool
from langchain.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)


class SQLDatabaseToolkit(BaseToolkit):
    """Toolkit for interacting with SQL databases."""

    db: SQLDatabase = Field(exclude=True)
    llm: BaseLanguageModel = Field(exclude=True)

    @property
    def dialect(self) -> str:
        """Return string representation of dialect to use."""
        return self.db.dialect

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        query_sql_database_tool_description = (
            "此工具的输入是详细且正确的SQL查询，输出是来自数据库的结果。如果查询不正确，将返回错误消息。"
            "请先使用sql_db_schema工具获取查询语句中用到的表的表结构。再使用sql_db_query工具创建正确的查询语句。"
        )
        info_sql_database_tool_description = (
            """此工具的输入是以逗号分隔的表列表，输出是这些表的架构和示例行。
            首先，通过调用list_tables_sql_db来确保表确实存在！
            示例输入：list1、list2、list3"""

        )
        return [
            QuerySQLDataBaseTool(
                db=self.db, description=query_sql_database_tool_description
            ),
            InfoSQLDatabaseTool(
                db=self.db, description=info_sql_database_tool_description
            ),
            ListSQLDatabaseTool(db=self.db),
            QuerySQLCheckerTool(db=self.db, llm=self.llm),
        ]
