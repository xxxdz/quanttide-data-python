import uuid

from pydantic import BaseModel, Field
from typing import List, Optional


class Table(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="id")
    name: str = Field(..., description="表名")
    columns: List[str] = Field(..., description="表的列名列表")
    description: Optional[str] = Field(None, description="表的描述")


class Dataset(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="id")
    name: str = Field(..., description="数据集的名称")
    table_name: str = Field(..., description="关联的表名")
    columns: List[str] = Field(..., description="包含的列")
    DataDocument: Optional[str] = Field(None, description="数据集的数据文档,用于描述")


class DataDirectory(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="id")
    name: str = Field(..., description="数据目录的名称")
    tables: List[Table] = Field(default_factory=list, description="数据目录中包含的表")
    datasets: List[Dataset] = Field(default_factory=list, description="数据目录中包含的数据集")
    description: Optional[str] = Field(None, description="数据目录的描述信息")


class DataProcessor(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="id")
    name: str = Field(..., description="数据处理器的名称")
    operation: str = Field(..., description="数据处理的操作类型，例如 'filter', 'aggregate', 'transform'")
    status: str = Field(..., description="数据处理器状态,active/inactive")
    input_datasets: List[Dataset] = Field(..., description="输入的数据集")
    output_dataset: Dataset = Field(..., description="输出的数据集")

    def run(self):
        pass


class Schema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="id")
    name: str = Field(..., description="Scheme名称")
    tables: List[Table] = Field(default_factory=list, description="Schema中包含的表列表")
    datasets: List[Dataset] = Field(default_factory=list, description="Schema中数据集列表")
    processors: List[DataProcessor] = Field(default_factory=list, description="Schema中处理器列表")
    directories: List[DataDirectory] = Field(default_factory=list, description="Schema中数据目录列表")


class Catalog(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="id")
    name: str = Field(..., description="Catalog的名称")
    schemas: List[Schema] = Field(default_factory=list, description="Catalog中的Schema列表")
    DataDocument: Optional[str] = Field(None, description="catalog的数据文档,用于描述")


class Dataspace(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="id")
    name: str = Field(..., description="数据空间的名称")
    catalogs: List[Catalog] = Field(default_factory=list, description="数据空间中catalog的列表")


# 示例数据
if __name__ == "__main__":
    # 创建示例 Table 对象
        table1 = Table(name="users", columns=["id", "name", "email"], description="用户信息表")
        table2 = Table(name="orders", columns=["id", "user_id", "amount"], description="订单信息表")

        # 创建示例 Dataset 对象
        dataset1 = Dataset(name="user_data", table_name="users", columns=["id", "name"],
                           DataDocument="用户基本信息数据文档")
        dataset2 = Dataset(name="order_data", table_name="orders", columns=["id", "amount"],
                           DataDocument="订单数据文档")

        # 创建示例 DataDirectory 对象
        data_directory = DataDirectory(
            name="default_directory",
            tables=[table1, table2],
            datasets=[dataset1, dataset2],
            description="默认的数据目录"
        )

        # 创建示例 DataProcessor 对象
        data_processor = DataProcessor(
            name="Filter Processor",
            operation="filter",
            status="active",
            input_datasets=[dataset1],
            output_dataset=dataset2
        )

        # 创建示例 Schema 对象
        schema = Schema(
            name="default_schema",
            tables=[table1, table2],
            datasets=[dataset1, dataset2],
            processors=[data_processor],
            directories=[data_directory]
        )

        # 创建示例 Catalog 对象
        catalog = Catalog(
            name="default_catalog",
            schemas=[schema],
            DataDocument="Catalog的描述文档"
        )

        # 创建 Dataspace 对象
        dataspace = Dataspace(
            name="default_dataspace",
            catalogs=[catalog]
        )

        # 打印 Dataspace 对象
        print(dataspace.model_dump_json(indent=4))
