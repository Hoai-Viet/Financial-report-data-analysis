import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format, current_timestamp, sum, lit, split, when, avg, count
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, DecimalType
import datetime
from datetime import date
from pyspark.sql.window import Window
from pyspark.sql import functions as F

spark = (SparkSession.builder
         .appName("bao-cao-tai-chinh")
         .getOrCreate())

"""
# Chuyển định dạng xlsx -> csv
pd.read_excel(r"inputdata/fact_kpi_month_raw_data_sheet0.xlsx",
              sheet_name="Sheet1", engine="openpyxl").to_csv(
                r"inputdata/fact_kpi_month_raw_data_sheet0.csv", index=False  
              )
pd.read_excel(r"inputdata/fact_kpi_month_raw_data_sheet1.xlsx",
              sheet_name="Sheet1", engine="openpyxl").to_csv(
                r"inputdata/fact_kpi_month_raw_data_sheet1.csv", index=False
              )
pd.read_excel(r"inputdata/fact_kpi_month_raw_data_sheet2.xlsx",
              sheet_name="Sheet1", engine="openpyxl").to_csv(
                r"inputdata/fact_kpi_month_raw_data_sheet2.csv", index=False
              )
pd.read_excel(r"inputdata/kpi_asm_data_202305.xlsx",
              sheet_name="KPI_ASM_DATA", engine="openpyxl").to_csv(
                r"inputdata/kpi_asm_data_202305.csv", index=False
              )
pd.read_excel(r"inputdata/fact_txn_month_raw_data.xlsx",
              sheet_name="Sheet0", engine="openpyxl").to_csv(
                  r"inputdata/fact_txn_month_raw_data.csv", index=False
              )

# df_dim_area
schema = StructType([
    StructField("area_id", IntegerType(), True),
    StructField("area_code", StringType(), True),
    StructField("area_name", StringType(), True)
])


df_dim_area = [(0, "A", "Hội Sở"), 
               (1, "B", "Đông Bắc Bộ"),
               (2, 'C', 'Tây Bắc Bộ'),
               (3, 'D', 'Đồng Bằng Sông Hồng'),
               (4, 'E', 'Bắc Trung Bộ'),
               (5, 'F', 'Nam Trung Bộ'),
               (6, 'G', 'Tây Nam Bộ'),
               (7, 'H', 'Đông Nam Bộ')]

df_dim_area = spark.createDataFrame(df_dim_area, schema=schema)\
    .withColumn("rec_created_dt", current_timestamp()) \
    .withColumn("rec_updated_dt", current_timestamp())

df_dim_area.coalesce(1).write.mode("overwrite").option("header", True).csv("dim_table/dim_area")

# df_dim_staff
schema = StructType([
    StructField("sm_id", IntegerType()),
    StructField("sm_name", StringType()),
    StructField("sm_email", StringType()),
    StructField("area_key", IntegerType())
])

df_dim_staff = [(0,'Nguyễn Thị Hồng','hong.nguyenthi@hocnghiepvu.com',4),
		    (1,'Trần Văn Tuấn Anh','anh.tranvantuan@hocnghiepvu.com',3),
		    (2,'Lê Thị Linh','linh.lethi@hocnghiepvu.com',4),
		    (3,'Phạm Minh Tuấn','tuan.phamminh@hocnghiepvu.com',4),
            (4,'Hoàng Thị Ngọc','ngoc.hoangthi@hocnghiepvu.com',6),
            (5,'Đặng Văn Đức','duc.dangvan@hocnghiepvu.com',4),
            (6,'Vũ Thị Mai','mai.vuthi@hocnghiepvu.com',3),
            (7,'Nguyễn Văn Khánh','khanh.nguyenvan@hocnghiepvu.com',3),
            (8,'Lê Thị Thu','thu.lethi@hocnghiepvu.com',3),
            (9,'Trần Minh Quân','quan.tranminh@hocnghiepvu.com',3),
            (10,'Phạm Thị Hạnh','hanh.phamthi@hocnghiepvu.com',6),
            (11,'Đinh Văn Hùng','hung.dinhvan@hocnghiepvu.com',3),
            (12,'Trần Thị Mai','mai.tranthi@hocnghiepvu.com',7),
            (13,'Lê Văn Tuấn','tuan.levan@hocnghiepvu.com',3),
            (14,'Nguyễn Thị Thanh','thanh.nguyenthi@hocnghiepvu.com',3),
            (15,'Hoàng Văn Nam','nam.hoangvan@hocnghiepvu.com',3),
            (16,'Trần Thị Thu','thu.tranthi@hocnghiepvu.com',6),
            (17,'Lê Minh Đức','duc.leminh@hocnghiepvu.com',1),
            (18,'Nguyễn Thị Bích','bich.nguyenthi@hocnghiepvu.com',6),
            (19,'Phạm Văn Hải','hai.phamvan@hocnghiepvu.com',3),
            (20,'Hoàng Thị Hà','ha.hoangthi@hocnghiepvu.com',5),
            (21,'Lê Văn Thành','thanh.levan@hocnghiepvu.com',7),
            (22,'Nguyễn Thị Ngọc','ngoc.nguyenthi@hocnghiepvu.com',1),
            (23,'Trần Văn Minh','minh.tranvan@hocnghiepvu.com',1),
            (24,'Lê Thị Phương','phuong.lethi@hocnghiepvu.com',6),
            (25,'Phạm Văn Đức','duc.phamvan@hocnghiepvu.com',3),
            (26,'Nguyễn Thị Mai','mai.nguyenthi@hocnghiepvu.com',3),
            (27,'Trần Văn Hùng','hung.tranvan@hocnghiepvu.com',1),
            (28,'Đỗ Thị Thu','thu.dothi@hocnghiepvu.com',5),
            (29,'Lê Văn Hải','hai.levan@hocnghiepvu.com',7),
            (30,'Phạm Thị Hương','huong.phamthi@hocnghiepvu.com',3),
            (31,'Nguyễn Văn Đoàn','doan.nguyenvan@hocnghiepvu.com',3),
            (32,'Lê Thị Thảo','thao.lethi@hocnghiepvu.com',3),
            (33,'Trần Văn Tùng','tung.tranvan@hocnghiepvu.com',6),
            (34,'Hoàng Văn Tân','tan.hoangvan@hocnghiepvu.com',1),
            (35,'Lê Thị Thúy','thuy.lethi@hocnghiepvu.com',7),
            (36,'Nguyễn Văn Duy','duy.nguyenvan@hocnghiepvu.com',3),
            (37,'Phạm Thị Thuỷ','thuy.phamthi@hocnghiepvu.com',5),
            (38,'Trần Văn Nam','nam.tranvan@hocnghiepvu.com',6),
            (39,'Lê Thu Hương','huong.lethu@hocnghiepvu.com',7),
            (40,'Hoàng Văn Đại','dai.hoangvan@hocnghiepvu.com',3),
            (41,'Nguyễn Thị Kim','kim.nguyenthi@hocnghiepvu.com',3),
            (42,'Trần Văn Bình','binh.tranvan@hocnghiepvu.com',3),
            (43,'Lê Thị Ngọc','ngoc.lethi@hocnghiepvu.com',7),
            (44,'Phạm Văn Thắng','thang.phamvan@hocnghiepvu.com',7),
            (45,'Đinh Thị Huệ','hue.dinhthi@hocnghiepvu.com',3),
            (46,'Trần Văn Hòa','hoa.tranvan@hocnghiepvu.com',1),
            (47,'Lê Thị Nga','nga.lethi@hocnghiepvu.com',7),
            (48,'Nguyễn Văn Tùng','tung.nguyenvan@hocnghiepvu.com',7),
            (49,'Phạm Thị Thanh','thanh.phamthi@hocnghiepvu.com',7),
            (50,'Hoàng Văn Hưng','hung.hoangvan@hocnghiepvu.com',6),
            (51,'Lê Thị Ánh','anh.lethi@hocnghiepvu.com',6),
            (52,'Nguyễn Văn Hà','ha.nguyenvan@hocnghiepvu.com',7),
            (53,'Trần Thị Hà','ha.tranthi@hocnghiepvu.com',5),
            (54,'Lê Văn Bình','binh.levan@hocnghiepvu.com',7),
            (55,'Nguyễn Thị Hằng','hang.nguyenthi@hocnghiepvu.com',7),
            (56,'Trần Văn Anh','anh.tranvan@hocnghiepvu.com',7),
            (57,'Hoàng Văn Lợi','loi.hoangvan@hocnghiepvu.com',7),
            (58,'Lê Thị Kim','kim.lethi@hocnghiepvu.com',7),
            (59,'Phạm Văn Đạo','dao.phamvan@hocnghiepvu.com',5),
            (60,'Trần Thị Hương','huong.tranthi@hocnghiepvu.com',6),
            (61,'Nguyễn Văn Hậu','hau.nguyenvan@hocnghiepvu.com',4),
            (62,'Lê Thị Hà','ha.lethi@hocnghiepvu.com',3),
            (63,'Hoàng Văn Bình','binh.hoangvan@hocnghiepvu.com',1),
            (64,'Đinh Thị Lan','lan.dinhthi@hocnghiepvu.com',6),
            (65,'Trần Văn Phú','phu.tranvan@hocnghiepvu.com',3),
            (66,'Nguyễn Văn Đức','duc.nguyenvan@hocnghiepvu.com',1),
            (67,'Nguyễn Văn Sơn','son.nguyenvan@hocnghiepvu.com',2),
            (68,'Phạm Thị Lan','lan.phamthi@hocnghiepvu.com',2),
            (69,'Nguyễn Văn Hải','hai.nguyenvan@hocnghiepvu.com',2),
            (70,'Lê Thị Hương','huong.lethi@hocnghiepvu.com',2),
            (71,'Trần Văn Thắng','thang.tranvan@hocnghiepvu.com',2),
            (72,'Hoàng Thị Thuận','thuan.hoangthi@hocnghiepvu.com',2),
            (73,'Lê Thu Thủy','thuy.lethu@hocnghiepvu.com',2)]

df_dim_staff = spark.createDataFrame(df_dim_staff, schema=schema).withColumn("rec_created_dt", current_timestamp()) \
                .withColumn("rec_updated_dt", current_timestamp())

df_dim_staff.coalesce(1).write.option("header", True).mode("overwrite").csv("dim_table/dim_staff")

# df_dim_date
from pyspark.sql.types import DateType
from pyspark.sql.functions import year, month, dayofmonth
import datetime

schema = StructType([
    StructField("date", DateType(), True)
])

# Mỗi row phải là tuple
data = [
    (datetime.date(2025, 1, 31),),
    (datetime.date(2025, 2, 28),),
    (datetime.date(2025, 3, 31),),
    (datetime.date(2025, 4, 30),),
    (datetime.date(2025, 5, 31),)
]

df_dim_date = spark.createDataFrame(data, schema=schema) \
                .withColumn("year", year("date")) \
                .withColumn("month", month("date")) \
                .withColumn("day", dayofmonth("date"))

df_dim_date.coalesce(1).write.option("header", True).mode("overwrite").csv("dim_table/dim_date")

# dim_funding_id

from pyspark.sql.types import (
    StructType, StructField,
    IntegerType, FloatType, DoubleType, StringType
)

schema = StructType([
    StructField("funding_id", IntegerType()),
    StructField("funding_code", StringType()),
    StructField("funding_name", StringType()),
    StructField("funding_parent_id", StringType()),
    StructField("funding_level", IntegerType()),
    StructField("sortorder", IntegerType())
])

data = [(1, 'PBT', '1. Lợi nhuận trước thuế', -1, 0, 1000000),
        (7, 'PBT01001', 'Thu nhập từ hoạt động thẻ', 2, 2, 1010000),
        (10, 'PBT010010001', 'Lãi trong hạn', 3, 3, 1010100),
        (11, 'PBT010010002', 'Lãi quá hạn', 3, 3, 1010101),
        (12, 'PBT010010003', 'Phí bảo hiểm', 3, 3, 1010102),
        (13, 'PBT010010004', 'Phí tăng hạn mức', 3, 3, 1010103),
        (14, 'PBT010010005', 'Phí thanh toán chậm, thu từ ngoại bảng, khác,…', 3, 3, 1010104),
        (8, 'PBT01002', 'Chi phí thuần KDV', 2, 2, 1020000),
        (15, 'PBT010020001', 'CP vốn TT2', 4, 3, 1020100),
        (16, 'PBT010020002', 'CP vốn CCTG', 4, 3, 1020101),
        (9, 'PBT01003', 'Chi phí thuần hoạt động khác', 2, 2, 1030000),
        (17, 'PBT010030001', 'DT Kinh doanh', 5, 3, 1030100),
        (18, 'PBT010030002', 'CP hoa hồng', 5, 3, 1030101),
        (19, 'PBT010030003', 'CP thuần KD khác', 5, 3, 1030102),
        (4, 'PBT01', 'Tổng thu nhập hoạt động', 1, 1, 1040000),
        (5, 'PBT02', 'Tổng chi phí hoạt động', 1, 1, 1050000),
        (20, 'PBT02001', 'CP nhân viên', 6, 2, 1050100),
        (21, 'PBT02002', 'CP quản lý', 6, 2, 1050101),
        (22, 'PBT02003', 'CP tài sản', 6, 2, 1050102),
        (6, 'PBT03', 'Chi phí dự phòng', 1, 1, 1060000),
        (2, 'SM', '2. Số lượng nhân sự (Sale Manager)', -1, 0, 2000000),
        (3, 'FR', '3. Chỉ số tài chính', -1, 0, 3000000),
        (23, 'FR01', 'CIR (%)', 7, 1, 3010100),
        (24, 'FR02', 'Margin (%)', 7, 1, 3010101),
        (25, 'FR03', 'Hiệu suất trên/vốn (%)', 7, 1, 3010102),
        (26, 'FR04', 'Hiệu suất BQ/ Nhân sự', 7, 1, 3010103)]

df_dim_funding_id = spark.createDataFrame(data, schema=schema).withColumn("rec_created_dt", current_timestamp()) \
        .withColumn("rec_updated_dt", current_timestamp())

df_dim_funding_id.coalesce(1).write.option("header", True).mode("overwrite").csv("dim_table/dim_funding_id")

# fact_summary_report_monthly
schema_fact_summary_report_monthly = StructType([
    StructField("month_key", IntegerType(), True),
    StructField("area_key", IntegerType(), True),
    StructField("report_id", IntegerType(), True),
    StructField("amt_dist_ytm_from_gl", DoubleType(), True),
    StructField("amt_dist_ytm_from_gl_final", DoubleType(), True)
])

# asm_rank_report
schema_asm_rank_report = StructType([
    StructField("month_key", IntegerType(), True),
    StructField("area_cde", StringType(), True),
    StructField("area_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("final_score", IntegerType(), True),
    StructField("rank_final", IntegerType(), True),
    StructField("ltn_avg", DoubleType(), True),
    StructField("rank_ltn", IntegerType(), True),
    StructField("psdn_avg", DoubleType(), True),
    StructField("rank_psdn", IntegerType(), True),
    StructField("approval_rate_avg", DoubleType(), True),
    StructField("rank_approval_rate", IntegerType(), True),
    StructField("npl_truoc_wo_luy_ke", DoubleType(), True),
    StructField("rank_npl_truoc_wo_luy_ke", IntegerType(), True),
    StructField("scale_score", IntegerType(), True),
    StructField("rank_ptkd", IntegerType(), True),
    StructField("cir", DoubleType(), True),
    StructField("rank_cir", IntegerType(), True),
    StructField("margin", DoubleType(), True),
    StructField("rank_margin", IntegerType(), True),
    StructField("hs_von", DoubleType(), True),
    StructField("rank_hs_von", IntegerType(), True),
    StructField("hsbq_nhan_su", DoubleType(), True),
    StructField("rank_hsbq_nhan_su", IntegerType(), True),
    StructField("fin_score", IntegerType(), True),
    StructField("rank_fin", IntegerType(), True)
])

# fact_summary_report_monthly
df_fact_summary_report_monthly = spark.createDataFrame([], schema_fact_summary_report_monthly)
df_fact_summary_report_monthly.coalesce(1).write.option("header", True).mode("overwrite").csv("bao_cao_output/fact_summary_report_monthly")

# asm_rank_report
df_asm_rank_report = spark.createDataFrame([], schema_asm_rank_report)
df_asm_rank_report.coalesce(1).write.option("header", True).mode("overwrite").csv("bao_cao_output/asm_rank_report")
"""

df_raw_fact_txn = spark.read.option("header", "true").option("inferSchema", "true").csv("inputdata/fact_txn_month_raw_data.csv")

# Thêm cột monthkey
df_fact_txn0 = df_raw_fact_txn.withColumn(
    "monthkey",
    date_format(col("transaction_date"), "yyyyMM").cast("int") + 200
)

# Tách mã cột analysis_code
df_fact_txn1 = df_raw_fact_txn.withColumn(
    "area_code",
    when(
        split(col("analysis_code"), "\.").getItem(2) == "00",
        "A"
    ).otherwise(split(col("analysis_code"), "\.").getItem(2))
)

# Tạo thêm cột funding id
df_fact_txn2 = df_fact_txn1.withColumn(
    "funding_id",
    when(col("account_code").isin("702000030002", "702000030001", "702000030102"), 10) 
    .when(col("account_code").isin("702000030012", "702000030112"), 11) 
    .when(col("account_code") == 716000000001, 12) 
    .when(col("account_code") == 719000030002, 13)
    .when(col("account_code").isin("719000030003", "719000030103", "790000030003", "790000030103", "790000030004", "790000030104"), 14) 
    .when(col("account_code") == 803000000001, 16) 
    .when(col("account_code").isin("801000000001", "802000000001"), 15) 
    .when(col("account_code").isin("816000000001", "816000000002", "816000000003"), 18)
    .when(col("account_code").isin("809000000002", "809000000001", "811000000001", "811000000102", "811000000002", "811014000001", 
                                  "811037000001", "811039000001", "811041000001", "815000000001", "819000000002", "819000000003", 
                                  "819000000001", "790000000003", "790000050101", "790000000101", "790037000001", "849000000001", 
                                  "899000000003", "899000000002", "811000000101", "819000060001"), 19) 
    .when(col("account_code").isin("702000010001", "702000010002", "704000000001", "705000000001", "709000000001", "714000000002", 
                                  "714000000003", "714037000001", "714000000004", "714014000001", "715000000001", "715037000001", 
                                  "719000000001", "709000000101", "719000000101"), 17) 
    .when(col("account_code").like("85%"), 20) 
    .when(col("account_code").like("86%"), 21) 
    .when(col("account_code").like("87%"), 22) 
    .when(col("account_code").isin("790000050001", "882200050001", "790000030001", "882200030001", "790000000001", "790000020101", 
                                  "882200000001", "882200050101", "882200020101", "882200060001", "790000050101", "882200030101"), 6)
    .otherwise(-1)
)

df_fact_txn3 = df_fact_txn2.join(dim_area, on="area_code").select("transaction_date", "account_code", "amount", "area_id", "funding_id")

from pyspark.sql.functions import date_format, col
df_fact_txn4 = df_fact_txn3.withColumn(
    "month_key",
    (date_format(col("transaction_date"), "yyyyMM").cast("int") + 200)
)

# Lưu file fact_txn
df_fact_txn = df_fact_txn4.select("month_key", "account_code", "amount", "area_id", "funding_id")

df_fact_txn = df_fact_txn.withColumnRenamed("area_id", "area_key")

df_fact_txn.coalesce(1).write.option("header", True).mode("overwrite").csv("input/fact_txn")

# Đọc data
df_sheet0 = (spark.read.option("header", "true").option("inferSchema", "true").csv("inputdata/fact_kpi_month_raw_data_sheet0.csv"))
df_sheet1 = (spark.read.option("header", "true").option("inferSchema", "true").csv("inputdata/fact_kpi_month_raw_data_sheet1.csv"))
df_sheet2 = (spark.read.option("header", "true").option("inferSchema", "true").csv("inputdata/fact_kpi_month_raw_data_sheet2.csv"))
df_kpi_asm = (spark.read.option("header", "true").option("inferSchema", "true").csv("inputdata/kpi_asm_data_202305.csv"))

# Nối 3 sheet
df_fact_kpi_month_raw_data = df_sheet0.unionByName(df_sheet1).unionByName(df_sheet2)

df_fact_kpi1 = df_fact_kpi_month_raw_data.withColumn(
    "area_key",
    when(col("pos_city").isin('Bắc Giang', 'Bắc Kạn', 'Cao Bằng', 'Hà Giang', 'Lạng Sơn', 'Phú Thọ', 'Quảng Ninh', 'Thái Nguyên', 'Tuyên Quang'), 1)
    .when(col("pos_city").isin('Điện Biên', 'Hòa Bình', 'Lai Châu', 'Lào Cai', 'Sơn La', 'Yên Bái'), 2)
    .when(col("pos_city").isin('Bắc Ninh', 'Hà Nam', 'Hà Nội', 'Hải Dương', 'Hải Phòng', 'Hưng Yên', 'Nam Định', 'Ninh Bình', 'Thái Bình', 'Vĩnh Phúc'), 3)
    .when(col("pos_city").isin('Hà Tĩnh', 'Huế', 'Nghệ An', 'Quảng Bình', 'Quảng Trị', 'Thanh Hóa'), 4)
    .when(col("pos_city").isin('Bình Định', 'Bình Thuận', 'Đà Nẵng', 'Đắk Lắk', 'Đắk Nông', 'Gia Lai', 'Khánh Hòa', 'Kon Tum', 'Lâm Đồng', 'Ninh Thuận', 'Phú Yên', 'Quảng Nam', 'Quảng Ngãi'), 5)
    .when(col("pos_city").isin('Cần Thơ', 'Đồng Tháp', 'Hậu Giang', 'Kiên Giang', 'Long An', 'Sóc Trăng', 'Tiền Giang', 'Trà Vinh', 'Vĩnh Long', 'An Giang', 'Bạc Liêu', 'Bến Tre', 'Cà Mau'), 6)
    .when(col("pos_city").isin('Bà Rịa - Vũng Tàu', 'Bình Dương', 'Bình Phước', 'Đồng Nai', 'Hồ Chí Minh', 'Tây Ninh'), 7)
)

df_fact_kpi2 = df_fact_kpi1.withColumn(
    "month_key",
    col("kpi_month") + 200
).withColumn(
    "write_off_month",
    (col("write_off_month") + 200).cast(IntegerType())
)

df_fact_kpi3 = df_fact_kpi2.fillna({"max_bucket": 1})

df_fact_kpi = df_fact_kpi3.select("month_key", "pos_cde", "pos_city", "application_id", "outstanding_principal", "write_off_month",
                                  "write_off_balance_principal", "psdn", "max_bucket", "area_key")

# Lưu file fact_kpi
df_fact_kpi.coalesce(1).write.option("header", True).mode("overwrite").csv("input/fact_kpi")

# tmp_report_gl_by_area_monthly
schema_tmp_report_gl_by_area_monthly = StructType([
    StructField("month_key", IntegerType(), True),
    StructField("funding_id", IntegerType(), True),
    StructField("area_key", IntegerType(), True),
    StructField("value", DoubleType(), True)   # float8 -> DoubleType
])

# tmp_total_dbt_staff_each_area_and_month
schema_tmp_total_dbt_staff_each_area_and_month = StructType([
    StructField("month_key", IntegerType(), True),
    StructField("area_key", IntegerType(), True),
    StructField("total_debt_aft_wo_grp1", DoubleType(), True),
    StructField("total_debt_aft_wo_grp2", DoubleType(), True),
    StructField("total_debt_aft_wo_grp2_5", DoubleType(), True),
    StructField("total_debt_aft_wo", DoubleType(), True),
    StructField("total_wo", DoubleType(), True),
    StructField("total_wo_next_month", DoubleType(), True)
])

# tmp_total_dist_debt_staff_monthly
schema_tmp_total_dist_debt_staff_monthly = StructType([
    StructField("month_key", IntegerType(), True),
    StructField("area_key", IntegerType(), True),
    StructField("debt_aft_wo", DoubleType(), True),
    StructField("debt_aft_wo_grp1", DoubleType(), True),
    StructField("debt_aft_wo_grp2", DoubleType(), True),
    StructField("debt_aft_wo_grp2345", DoubleType(), True),
    StructField("debt_bef_wo_grp2345", DoubleType(), True),
    StructField("psdn", DoubleType(), True),
    StructField("amount_sm", DoubleType(), True),
    StructField("npl_grp345", DoubleType(), True),
    StructField("cum_wo", DoubleType(), True),
    StructField("debt_aft_wo_month", DoubleType(), True)
])

# tmp_ratio_each_area_to_all_area
schema_tmp_ratio_each_area_to_all_area = StructType([
    StructField("month_key", IntegerType(), True),
    StructField("area_key", IntegerType(), True),
    StructField("ratio_debt_aft_wo_grp1", DoubleType(), True),
    StructField("ratio_debt_aft_wo_grp2", DoubleType(), True),
    StructField("ratio_debt_aft_wo_grp2345", DoubleType(), True),
    StructField("ratio_bef_aft_wo_grp2345", DoubleType(), True),
    StructField("ratio_psdn", DoubleType(), True),
    StructField("ratio_sm", DoubleType(), True),
    StructField("ratio_debt_aft_wo", DoubleType(), True)
])

# Lưu các bảng vào df
dim_area = spark.read.option("header", True).option("inferSchema", True).csv("dim_table/dim_area")
dim_staff = spark.read.option("header", True).option("inferSchema", True).csv("dim_table/dim_staff")
dim_date = spark.read.option("header", True).option("inferSchema", True).csv("dim_table/dim_date")
dim_funding_id = spark.read.option("header", True).option("inferSchema", True).csv("dim_table/dim_funding_id")

fact_summary_report_monthly = spark.read.option("header", True).option("inferSchema", True).csv("bao_cao_output/fact_summary_report_monthly")
asm_rank_report = spark.read.option("header", True).option("inferSchema", True).csv("bao_cao_output/asm_rank_report")
fact_txn = spark.read.option("header", True).option("inferSchema", True).csv("input/fact_txn")
fact_kpi = spark.read.option("header", True).option("inferSchema", True).csv("input/fact_kpi")

# fct_summary_report_asm_ranked_monthly_function
def tmp_table(p_date):
    # Set biến month_key tại thời điểm muốn xem báo cáo
    if p_date == None:
        vProcess_Month = int(datetime.now().strftime("%Y%m"))
    else:
        vProcess_Month = int(p_date.strftime("%Y%m"))

    # Tạo dữ liệu mới cho tmp_report_gl_by_area_monthly tại thời điểm muốn xem báo cáo
    df_tmp_report_gl_by_area_monthly = fact_txn.where((col("month_key") <= vProcess_Month) & (col("funding_id") > 0)) \
                 .groupBy("funding_id", "area_key") \
                 .agg(sum("amount").cast(DecimalType(20,2)).alias("value")) \
                 .withColumn("month_key", lit(vProcess_Month)) \
                 .select("month_key", "funding_id", "area_key", "value")
    
    df_tmp_report_gl_by_area_monthly.write.mode("overwrite").parquet("tmp_table/tmp_report_gl_by_area_monthly")
    
    # Tổng dư nợ mỗi kỳ mỗi khu vực
    df_tmp_total_dbt_staff_each_area_and_month0 = fact_kpi.where(col("month_key") <= vProcess_Month) \
                                                .groupBy("month_key", "area_key") \
                                                .agg(
                                                    sum(when(col("max_bucket") == 1, col("outstanding_principal"))).cast(DecimalType(20, 2)).alias("total_debt_aft_wo_grp1"),
                                                    sum(when(col("max_bucket") == 2, col("outstanding_principal"))).cast(DecimalType(20, 2)).alias("total_debt_aft_wo_grp2"),
                                                    sum(when((col("max_bucket") >= 2) & (col("max_bucket") <= 5), col("outstanding_principal"))).cast(DecimalType(20, 2)).alias("total_debt_aft_wo_grp2_5"),
                                                    sum(col("outstanding_principal")).cast(DecimalType(20, 2)).alias("total_debt_aft_wo"),
                                                )
    # Tổng write-off tháng hiện tại và tiếp theo
    df_tmp_total_dbt_staff_each_area_and_month1 = fact_kpi.where((col("month_key") <= vProcess_Month) & (col("write_off_month") == col("month_key"))) \
                                                .groupBy("month_key", "area_key", "write_off_month") \
                                                .agg(
                                                    sum("write_off_balance_principal").cast(DecimalType(20,2)).alias("total_wo")
                                                )

    # Tạo partition
    w = Window.partitionBy("area_key").orderBy(col("write_off_month").desc())

    df_tmp_total_dbt_staff_each_area_and_month2 = df_tmp_total_dbt_staff_each_area_and_month1.withColumn(
        "total_wo_next_month",
        F.lead("total_wo", 1, 0).over(w)
    ).drop("write_off_month")

    df_tmp_total_dbt_staff_each_area_and_month = df_tmp_total_dbt_staff_each_area_and_month0.join(df_tmp_total_dbt_staff_each_area_and_month2, 
                                                                                                  on=["area_key","month_key"],
                                                                                                  how="inner")
    
    df_tmp_total_dbt_staff_each_area_and_month.write.mode("overwrite").parquet("tmp_table/tmp_total_dbt_staff_each_area_and_month")

    # Dư nợ bình quân cuối kỳ toàn khu vực
    # Tổng toàn khu vực
    df_tmp_total_dist_debt_staff_monthly0 = (
    df_tmp_total_dbt_staff_each_area_and_month
    .where(col("month_key") <= vProcess_Month)
    .groupBy("month_key")
    .agg(
        sum("total_debt_aft_wo").alias("total_dbt_aft"),
        sum("total_debt_aft_wo_grp1").alias("total_dbt_aft_grp1"),
        sum("total_debt_aft_wo_grp2").alias("total_dbt_aft_grp2"),
        sum("total_debt_aft_wo_grp2_5").alias("total_dbt_aft_grp2345")
    )
    .agg(
        avg("total_dbt_aft").cast(DecimalType(20,2)).alias("avg_dbt_aft"),
        avg("total_dbt_aft_grp1").cast(DecimalType(20,2)).alias("avg_dbt_aft_grp1"),
        avg("total_dbt_aft_grp2").cast(DecimalType(20,2)).alias("avg_dbt_aft_grp2"),
        avg("total_dbt_aft_grp2345").cast(DecimalType(20,2)).alias("avg_dbt_aft_grp2345")
    )
    .withColumn("month_key", lit(vProcess_Month))
    .withColumn("area_key", lit(0))
    .select("month_key", "area_key", "avg_dbt_aft",
            "avg_dbt_aft_grp1","avg_dbt_aft_grp2","avg_dbt_aft_grp2345")
    )

    # Số dư cuối kỳ lũy kế của toàn khu vực trước wo nhóm 2,3,4,5
    df_tmp_total_dist_debt_staff_monthly1 = (
        df_tmp_total_dbt_staff_each_area_and_month.where(col("month_key") <= vProcess_Month) 
        .agg(
            sum(
                col("total_debt_aft_wo_grp2_5") +
                col("total_wo") +
                col("total_wo_next_month")
            ).alias("total_dbt_bef_grp2345")
        )
        .withColumn("month_key", lit(vProcess_Month))
        .withColumn("area_key", lit(0))
        )
    
    # Tổng thẻ PSDN
    df_tmp_total_dist_debt_staff_monthly2 = (
        fact_kpi.where(col("month_key") <= vProcess_Month)
        .agg(
            count(col("psdn")).alias("psdn")
        )
        .withColumn("month_key", lit(vProcess_Month))
        .withColumn("area_key", lit(0))
    )

    # Tổng số lượng SM
    df_tmp_total_dist_debt_staff_monthly3 = (
        dim_staff.agg(
        count("*").alias("amount_sm") 
        )
        .withColumn("month_key", lit(vProcess_Month))
        .withColumn("area_key", lit(0))    
    )

    # Tổng npl tại tất cả vùng
    df_tmp_total_dist_debt_staff_monthly4 = (
        fact_kpi.where((col("month_key") == vProcess_Month) & (col("max_bucket").isin(3,4,5)))
                .agg(
                    sum("outstanding_principal").alias("npl_grp345")
                )
                .withColumn("month_key", lit(vProcess_Month))
                .withColumn("area_key", lit(0))  
    )

    # Lũy kế WO tất cả vùng 
    df_tmp_total_dist_debt_staff_monthly5 = (
        fact_kpi.where((col("month_key") <= vProcess_Month) & (col("write_off_month") == col("month_key")))
                .agg(
                    sum("write_off_balance_principal").cast(DecimalType(20,2)).alias("cum_wo")
                )
                .withColumn("month_key", lit(vProcess_Month))
                .withColumn("area_key", lit(0)) 
    )

    # tổng dư nợ của toàn vùng tại vProcess_Month
    df_tmp_total_dist_debt_staff_monthly6 = (
        fact_kpi.where(col("month_key") == vProcess_Month)
                .agg(
                    sum("outstanding_principal").alias("debt_aft_wo_month")
                )
                .withColumn("month_key", lit(vProcess_Month))
                .withColumn("area_key", lit(0)) 
    )

    df_tmp_total_dist_debt_staff_monthly7 = (
        df_tmp_total_dist_debt_staff_monthly0.join(df_tmp_total_dist_debt_staff_monthly1, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly2, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly3, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly4, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly5, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly6, ["month_key", "area_key"], "inner")
    )

    # Dư nợ bình quân cuối kỳ mỗi khu vực
    df_tmp_total_dist_debt_staff_monthly8 = (
        df_tmp_total_dbt_staff_each_area_and_month.where(col("month_key") <= vProcess_Month)
            .groupBy("month_key", "area_key")
            .agg(
                sum("total_debt_aft_wo").alias("total_dbt_aft"),
                sum("total_debt_aft_wo_grp1").alias("total_dbt_aft_grp1"),
                sum("total_debt_aft_wo_grp2").alias("total_dbt_aft_grp2"),
                sum("total_debt_aft_wo_grp2_5").alias("total_dbt_aft_grp2345")
            )
            .groupBy("area_key")
            .agg(
                avg("total_dbt_aft").cast(DecimalType(20,2)).alias("avg_dbt_aft"),
                avg("total_dbt_aft_grp1").cast(DecimalType(20,2)).alias("avg_dbt_aft_grp1"),
                avg("total_dbt_aft_grp2").cast(DecimalType(20,2)).alias("avg_dbt_aft_grp2"),
                avg("total_dbt_aft_grp2345").cast(DecimalType(20,2)).alias("avg_dbt_aft_grp2345")
            )
            .withColumn("month_key", lit(vProcess_Month))
            .select("month_key", "area_key", "avg_dbt_aft",
            "avg_dbt_aft_grp1","avg_dbt_aft_grp2","avg_dbt_aft_grp2345")
    )

    # Số dư cuối kỳ lũy kế của toàn khu vực trước wo nhóm 2,3,4,5
    df_tmp_total_dist_debt_staff_monthly9 = (
        df_tmp_total_dbt_staff_each_area_and_month.where(col("month_key") <= vProcess_Month) 
        .groupBy("area_key")
        .agg(
            sum(
                col("total_debt_aft_wo_grp2_5") +
                col("total_wo") +
                col("total_wo_next_month")
            ).alias("total_dbt_bef_grp2345")
        )
        .withColumn("month_key", lit(vProcess_Month))
    )
    
    # Tổng thẻ PSDN từng khu vực
    df_tmp_total_dist_debt_staff_monthly10 = (
        fact_kpi.where(col("month_key") <= vProcess_Month)
        .groupBy("area_key")
        .agg(
            count(col("psdn")).alias("psdn")
        )
        .withColumn("month_key", lit(vProcess_Month))
    )

    # Tổng số lượng SM từng khu vực
    df_tmp_total_dist_debt_staff_monthly11 = (
        dim_staff.groupBy("area_key")
        .agg(
        count("*").alias("amount_sm") 
        )
        .withColumn("month_key", lit(vProcess_Month)) 
    )

    # Tổng npl tại từng vùng
    df_tmp_total_dist_debt_staff_monthly12 = (
        fact_kpi.where((col("month_key") == vProcess_Month) & (col("max_bucket").isin(3,4,5)))
                .groupBy("area_key")
                .agg(
                    sum("outstanding_principal").alias("npl_grp345")
                )
                .withColumn("month_key", lit(vProcess_Month))
    )

    # Lũy kế WO tất cả vùng 
    df_tmp_total_dist_debt_staff_monthly13 = (
        fact_kpi.where((col("month_key") <= vProcess_Month) & (col("write_off_month") == col("month_key")))
                .groupBy("area_key")
                .agg(
                    sum("write_off_balance_principal").cast(DecimalType(20,2)).alias("cum_wo")
                )
                .withColumn("month_key", lit(vProcess_Month))
    )

    # tổng dư nợ của toàn vùng tại vProcess_Month
    df_tmp_total_dist_debt_staff_monthly14 = (
        fact_kpi.where(col("month_key") == vProcess_Month)
                .groupBy("area_key")
                .agg(
                    sum("outstanding_principal").alias("debt_aft_wo_month")
                )
                .withColumn("month_key", lit(vProcess_Month))
    )

    df_tmp_total_dist_debt_staff_monthly15 = (
        df_tmp_total_dist_debt_staff_monthly8.join(df_tmp_total_dist_debt_staff_monthly9, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly10, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly11, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly12, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly13, ["month_key", "area_key"], "inner")
                                            .join(df_tmp_total_dist_debt_staff_monthly14, ["month_key", "area_key"], "inner")
    )

    df_tmp_total_dist_debt_staff_monthly = df_tmp_total_dist_debt_staff_monthly7.unionByName(df_tmp_total_dist_debt_staff_monthly15)

    # Lưu parquet
    df_tmp_total_dist_debt_staff_monthly.write.mode("overwrite").parquet("tmp_table/tmp_total_dist_debt_staff_monthly")

    # Tỉ lệ dư nợ, staff, psdn tại mỗi vùng
    df_tmp_ratio_each_area_to_all_area0 = (
        df_tmp_total_dist_debt_staff_monthly.alias("t1")
    .join(
        df_tmp_total_dist_debt_staff_monthly.alias("t2"),
        (col("t1.month_key") == col("t2.month_key")) & (col("t2.area_key") == 0),
        "inner"
    )
    .where(col("t1.month_key") == vProcess_Month)
    .select(
        col("t1.month_key"),
        col("t1.area_key"),
        (col("t1.avg_dbt_aft_grp1").cast("float") / col("t2.avg_dbt_aft_grp1")).alias("ratio_debt_aft_wo_grp1"),
        (col("t1.avg_dbt_aft_grp2").cast("float") / col("t2.avg_dbt_aft_grp2")).alias("ratio_debt_aft_wo_grp2"),
        (col("t1.avg_dbt_aft_grp2345").cast("float") / col("t2.avg_dbt_aft_grp2345")).alias("ratio_debt_aft_wo_grp2345"),
        (col("t1.total_dbt_bef_grp2345").cast("float") / col("t2.total_dbt_bef_grp2345")).alias("ratio_bef_aft_wo_grp2345"),
        (col("t1.psdn") / col("t2.psdn").cast("float")).alias("ratio_psdn"),
        (col("t1.amount_sm").cast("float") / col("t2.amount_sm")).alias("ratio_sm"),
        (col("t1.avg_dbt_aft") / col("t2.avg_dbt_aft")).alias("ratio_debt_aft_wo")
    )
    )

    #Update area_key = 0
    df_tmp_ratio_each_area_to_all_area = (
        df_tmp_ratio_each_area_to_all_area0
        .withColumn("ratio_debt_aft_wo_grp1", when(col("area_key") == 0, 0).otherwise(col("ratio_debt_aft_wo_grp1")))
        .withColumn("ratio_debt_aft_wo_grp2", when(col("area_key") == 0, 0).otherwise(col("ratio_debt_aft_wo_grp2")))
        .withColumn("ratio_debt_aft_wo_grp2345", when(col("area_key") == 0, 0).otherwise(col("ratio_debt_aft_wo_grp2345")))
        .withColumn("ratio_bef_aft_wo_grp2345", when(col("area_key") == 0, 0).otherwise(col("ratio_bef_aft_wo_grp2345")))
        .withColumn("ratio_psdn", when(col("area_key") == 0, 0).otherwise(col("ratio_psdn")))
        .withColumn("ratio_sm", when(col("area_key") == 0, 0).otherwise(col("ratio_sm")))
        .withColumn("ratio_debt_aft_wo", when(col("area_key") == 0, 0).otherwise(col("ratio_debt_aft_wo")))
        )
    
    df_tmp_ratio_each_area_to_all_area = df_tmp_ratio_each_area_to_all_area.write.mode("overwrite").parquet("tmp_table/tmp_ratio_each_area_to_all_area")
                                     
    return df_tmp_ratio_each_area_to_all_area
 
df = tmp_table(date(2025,2,2))


# Đọc các bảng tmp
df_tmp_total_dist_debt_staff_monthly = spark.read.parquet("tmp_table/tmp_total_dist_debt_staff_monthly")
df_tmp_report_gl_by_area_monthly = spark.read.parquet("tmp_table/tmp_report_gl_by_area_monthly")
df_tmp_ratio_each_area_to_all_area = spark.read.parquet("tmp_table/tmp_ratio_each_area_to_all_area")
df_tmp_total_dbt_staff_each_area_and_month = spark.read.parquet("tmp_table/tmp_total_dbt_staff_each_area_and_month")

def fct_summary_report_asm_ranked_monthly(p_date):
    # Set biến month_key tại thời điểm muốn xem báo cáo
    if p_date == None:
        vProcess_Month = int(datetime.now().strftime("%Y%m"))
    else:
        vProcess_Month = int(p_date.strftime("%Y%m"))

    # Báo cáo tài chính từng khu vực
    # Funding_id chưa 6, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22
    df_fact_summary_report_monthly0 = (
        df_tmp_report_gl_by_area_monthly.alias("t1")
        .join(
            df_tmp_report_gl_by_area_monthly.alias("t2"),
            (col("t1.month_key") == col("t2.month_key")) & (col("t2.area_key") == 0) & (col("t1.funding_id") == col("t2.funding_id"))
        )
        .join(
            df_tmp_ratio_each_area_to_all_area.alias("tr"),
            (col("t1.month_key") == col("tr.month_key")) & (col("t1.area_key") == col("tr.area_key"))
        )
        .where((col("t1.month_key") == vProcess_Month) & (~col("t1.funding_id").isin(15,16)))
        .withColumn(
            "amt_dist_ytm_from_gl_final",
            when(col("t1.funding_id").isin(10, 13), col("t1.value") + col("ratio_debt_aft_wo_grp1") * col("t2.value"))
            .when(col("t1.funding_id") == 11, col("t1.value") + col("ratio_debt_aft_wo_grp2") * col("t2.value"))
            .when(col("t1.funding_id") == 12, col("t1.value") + col("ratio_psdn") * col("t2.value"))
            .when(col("t1.funding_id") == 14, col("t1.value") + col("ratio_bef_aft_wo_grp2345") * col("t2.value"))
            .when(col("t1.funding_id").isin(17, 18, 19), col("t1.value") + col("ratio_debt_aft_wo") * col("t2.value"))
            .when(col("t1.funding_id").isin(20, 21, 22), col("t1.value") + col("ratio_sm") * col("t2.value"))
            .when(col("t1.funding_id") == 6, col("t1.value") + col("ratio_bef_aft_wo_grp2345") * col("t2.value"))
            )
        .select(
            col("t1.month_key"),
            col("t1.area_key"),
            col("t1.funding_id").alias("report_id"),
            col("t1.value").alias("amt_dist_ytm_from_gl"),
            col("amt_dist_ytm_from_gl_final").cast(DecimalType(20, 2))
        )
    )

    # Funding id 15, 16
    df_fact_summary_report_monthly1 = (
        df_tmp_report_gl_by_area_monthly.alias("t1")
        .join(
            df_tmp_ratio_each_area_to_all_area.alias("tr"),
            col("t1.month_key") == col("tr.month_key"),
            "cross"
        )
        .where((col("t1.month_key") == vProcess_Month) & (col("t1.funding_id").isin(15,16)))
        .withColumn(
            "amt_dist_ytm_from_gl_final",
            when(col("value") * col("ratio_debt_aft_wo") == 0, col("value")).otherwise(col("value") * col("ratio_debt_aft_wo"))
        )
        .select(
            col("t1.month_key"),
            col("tr.area_key"),
            col("t1.funding_id").alias("report_id"),
            col("t1.value").alias("amt_dist_ytm_from_gl"),
            col("amt_dist_ytm_from_gl_final").cast(DecimalType(20, 2))
        )
    )

    df_fact_summary_report_monthly2 = df_fact_summary_report_monthly1.unionByName(df_fact_summary_report_monthly0)

    # Funding id 5, 7, 8, 9
    df_fact_summary_report_monthly3 = (
        df_fact_summary_report_monthly2.join(
            dim_funding_id,
            (col("funding_id") == col("report_id")) & (col("report_id") != 6)
            )
        .groupBy("funding_parent_id", "area_key")
        .agg(
            sum("amt_dist_ytm_from_gl").alias("amt_dist_ytm_from_gl"),
            sum("amt_dist_ytm_from_gl_final").alias("amt_dist_ytm_from_gl_final")
        )
        .withColumn(
            "report_id",
            when(col("funding_parent_id") == 3, 7)
            .when(col("funding_parent_id") == 4, 8)
            .when(col("funding_parent_id") == 5, 9)
            .when(col("funding_parent_id") == 6, 5)
        )
        .select(
            lit(vProcess_Month).alias("month_key"),
            col("area_key"),
            col("report_id"),
            col("amt_dist_ytm_from_gl"),
            col("amt_dist_ytm_from_gl_final")
        )
    )

    df_fact_summary_report_monthly4 = df_fact_summary_report_monthly3.unionByName(df_fact_summary_report_monthly2)

    df_fact_summary_report_monthly5 = (
        df_fact_summary_report_monthly4.join(
            dim_funding_id,
            col("funding_id") == col("report_id")
            )
        .where((col("month_key") == vProcess_Month) & (col("funding_parent_id") == 2))
        .groupBy("area_key")
        .agg(
            sum("amt_dist_ytm_from_gl").alias("amt_dist_ytm_from_gl"),
            sum("amt_dist_ytm_from_gl_final").alias("amt_dist_ytm_from_gl_final")
        )
        .select(
            lit(vProcess_Month).alias("month_key"),
            col("area_key"),
            lit(4).alias("report_id"),
            col("amt_dist_ytm_from_gl"),
            col("amt_dist_ytm_from_gl_final")
        )
    )

    df_fact_summary_report_monthly6 = df_fact_summary_report_monthly5.unionByName(df_fact_summary_report_monthly4)

    df_fact_summary_report_monthly7 = (
        df_fact_summary_report_monthly6.join(
            dim_funding_id,
            col("funding_id") == col("report_id")
            )
        .where((col("month_key") == vProcess_Month) & (col("funding_parent_id") == 1))
        .groupBy("area_key")
        .agg(
            sum("amt_dist_ytm_from_gl").alias("amt_dist_ytm_from_gl"),
            sum("amt_dist_ytm_from_gl_final").alias("amt_dist_ytm_from_gl_final")
        )
        .select(
            lit(vProcess_Month).alias("month_key"),
            col("area_key"),
            lit(1).alias("report_id"),
            col("amt_dist_ytm_from_gl"),
            col("amt_dist_ytm_from_gl_final")
        )
    )

    df_fact_summary_report_monthly8 = df_fact_summary_report_monthly7.unionByName(df_fact_summary_report_monthly6)

    df_fact_summary_report_monthly9 = (
        df_tmp_total_dist_debt_staff_monthly.select(
            lit(vProcess_Month).alias("month_key"),
            col("area_key"),
            lit(2).alias("report_id"),
            col("amount_sm").alias("amt_dist_ytm_from_gl"),
            col("amount_sm").alias("amt_dist_ytm_from_gl_final")
        )
    )

    df_fact_summary_report_monthly10 = df_fact_summary_report_monthly9.unionByName(df_fact_summary_report_monthly8)

    # CIR
    df_fact_summary_report_monthly11 = (
        df_fact_summary_report_monthly10.alias("t1")
        .join(
            df_fact_summary_report_monthly10.alias("t2"),
            (col("t1.area_key") == col("t2.area_key")) 
            & (col("t1.month_key") == col("t2.month_key"))
            & (col("t1.report_id") == 5) 
            & (col("t2.report_id") == 4)
        )
        .where(col("t1.month_key") == vProcess_Month)
        .select(
            lit(vProcess_Month).alias("month_key"),
            col("t1.area_key"),
            lit(23).alias("report_id"),
            (-col("t1.amt_dist_ytm_from_gl") / col("t2.amt_dist_ytm_from_gl") * 100).cast(DecimalType(20,2)).alias("amt_dist_ytm_from_gl"),
            (-col("t1.amt_dist_ytm_from_gl_final") / col("t2.amt_dist_ytm_from_gl_final") * 100).cast(DecimalType(20,2)).alias("amt_dist_ytm_from_gl_final")
        )
    )

    # Margin
    df_fact_summary_report_monthly12 = (
        df_fact_summary_report_monthly10.alias("t1")
        .join(
            df_fact_summary_report_monthly10.alias("t2"),
            (col("t1.area_key") == col("t2.area_key")) 
            & (col("t1.month_key") == col("t2.month_key"))
            & (col("t1.report_id") == 1) 
            & (col("t2.report_id") == 7)
        )
        .join(
            df_fact_summary_report_monthly10.alias("t3"),
            (col("t1.area_key") == col("t3.area_key")) 
            & (col("t1.month_key") == col("t3.month_key"))
            & (col("t3.report_id") == 17) 
        )
        .where(col("t1.month_key") == vProcess_Month)
        .select(
            lit(vProcess_Month).alias("month_key"),
            col("t1.area_key"),
            lit(24).alias("report_id"),
            (col("t1.amt_dist_ytm_from_gl") / (col("t2.amt_dist_ytm_from_gl") + col("t3.amt_dist_ytm_from_gl")) * 100).cast(DecimalType(20,2)).alias("amt_dist_ytm_from_gl"),
            (col("t1.amt_dist_ytm_from_gl_final") / (col("t2.amt_dist_ytm_from_gl_final") + col("t3.amt_dist_ytm_from_gl_final")) * 100).cast(DecimalType(20,2)).alias("amt_dist_ytm_from_gl_final")
        )
    )

    # Hiệu suất trên vốn bình quân%
    df_fact_summary_report_monthly13 = (
        df_fact_summary_report_monthly10.alias("t1")
        .join(
            df_fact_summary_report_monthly10.alias("t2"),
            (col("t1.area_key") == col("t2.area_key")) 
            & (col("t1.month_key") == col("t2.month_key"))
            & (col("t1.report_id") == 1) 
            & (col("t2.report_id") == 8)
        )
        .where(col("t1.month_key") == vProcess_Month)
        .select(
            lit(vProcess_Month).alias("month_key"),
            col("t1.area_key"),
            lit(25).alias("report_id"),
            (-col("t1.amt_dist_ytm_from_gl") / col("t2.amt_dist_ytm_from_gl") * 100).cast(DecimalType(20,2)).alias("amt_dist_ytm_from_gl"),
            (-col("t1.amt_dist_ytm_from_gl_final") / col("t2.amt_dist_ytm_from_gl_final") * 100).cast(DecimalType(20,2)).alias("amt_dist_ytm_from_gl_final")
        )
    )

    # Hiệu suất BQ/Nhân sự
    df_fact_summary_report_monthly14 = (
        df_fact_summary_report_monthly10.alias("t1")
        .join(
            df_fact_summary_report_monthly10.alias("t2"),
            (col("t1.area_key") == col("t2.area_key")) 
            & (col("t1.month_key") == col("t2.month_key"))
            & (col("t1.report_id") == 1) 
            & (col("t2.report_id") == 2)
        )
        .where(col("t1.month_key") == vProcess_Month)
        .select(
            lit(vProcess_Month).alias("month_key"),
            col("t1.area_key"),
            lit(26).alias("report_id"),
            (col("t1.amt_dist_ytm_from_gl") / col("t2.amt_dist_ytm_from_gl") * 100).cast(DecimalType(20,2)).alias("amt_dist_ytm_from_gl"),
            (col("t1.amt_dist_ytm_from_gl_final") / col("t2.amt_dist_ytm_from_gl_final") * 100).cast(DecimalType(20,2)).alias("amt_dist_ytm_from_gl_final")
        )
    )

    # Chỉ số tài chính
    df_fact_summary_report_monthly15 = (
        dim_area.select(
            lit(vProcess_Month).alias("month_key"),
            col("area_id").alias("area_key"),
            lit(3).alias("report_id"),
            lit(0).alias("amt_dist_ytm_from_gl"),
            lit(0).alias("amt_dist_ytm_from_gl_final")
        )
    )

    # Tỉ lệ nợ xấu NPL
    df_fact_summary_report_monthly16 = (
        df_tmp_total_dist_debt_staff_monthly.select(
            lit(vProcess_Month).alias("month_key"),
            col("area_key"),
            lit(27).alias("report_id"),
            lit(0).alias("amt_dist_ytm_from_gl"),
            ((col("cum_wo") + col("npl_grp345")) / (col("cum_wo") + col("debt_aft_wo_month")) * 100).cast(DecimalType(20,2)).alias("amt_dist_ytm_from_gl_final")
        )
    )

    df_fact_summary_report_monthly = df_fact_summary_report_monthly10.unionByName(df_fact_summary_report_monthly11).unionByName(df_fact_summary_report_monthly12) \
                                    .unionByName(df_fact_summary_report_monthly13).unionByName(df_fact_summary_report_monthly14).unionByName(df_fact_summary_report_monthly15) \
                                    .unionByName(df_fact_summary_report_monthly16)
    
    df_fact_summary_report_monthly.write.mode("overwrite").parquet("bao_cao_output/fact_summary_report_monthly")

    return df_fact_summary_report_monthly

df = fct_summary_report_asm_ranked_monthly(date(2025,2,2))
spark.conf.set("spark.sql.debug.maxToStringFields", 1000)

df_result = (
    dim_funding_id.alias("dim")
    .join(
        df.alias("fct"),
        (col("fct.report_id") == col("dim.funding_id"))
        & (col("fct.month_key").isin([202501, 202502, 202503, 202504, 202505])),
        "left"
    )
    .groupBy(
        col("fct.report_id"),
        col("dim.funding_name"),
        col("dim.sortorder"),
        col("fct.month_key")
    )
    .agg(
        sum(when(col("fct.area_key") == 0, col("fct.amt_dist_ytm_from_gl_final")).otherwise(0)).alias("HEAD"),
        sum(when(col("fct.area_key") == 1, col("fct.amt_dist_ytm_from_gl_final")).otherwise(0)).alias("Đông Bắc Bộ"),
        sum(when(col("fct.area_key") == 2, col("fct.amt_dist_ytm_from_gl_final")).otherwise(0)).alias("Tây Bắc Bộ"),
        sum(when(col("fct.area_key") == 3, col("fct.amt_dist_ytm_from_gl_final")).otherwise(0)).alias("Đồng Bằng Sông Hồng"),
        sum(when(col("fct.area_key") == 4, col("fct.amt_dist_ytm_from_gl_final")).otherwise(0)).alias("Bắc Trung Bộ"),
        sum(when(col("fct.area_key") == 5, col("fct.amt_dist_ytm_from_gl_final")).otherwise(0)).alias("Nam Trung Bộ"),
        sum(when(col("fct.area_key") == 6, col("fct.amt_dist_ytm_from_gl_final")).otherwise(0)).alias("Tây Nam Bộ"),
        sum(when(col("fct.area_key") == 7, col("fct.amt_dist_ytm_from_gl_final")).otherwise(0)).alias("Đông Nam Bộ"),
        sum(when(col("fct.area_key") != 0, col("fct.amt_dist_ytm_from_gl_final")).otherwise(0)).alias("total")
    )
    .select(
        col("dim.funding_name").alias("Báo Cáo Tổng Hợp"),
        "HEAD",
        "Đông Bắc Bộ",
        "Tây Bắc Bộ",
        "Đồng Bằng Sông Hồng",
        "Bắc Trung Bộ",
        "Nam Trung Bộ",
        "Tây Nam Bộ",
        "Đông Nam Bộ",
        "total",
        col("fct.month_key")
    )
    .orderBy("dim.sortorder")
)

df_result.show()

