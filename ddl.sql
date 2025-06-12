create table tmp_report_gl_by_area_monthly
(
	month_key int,
	funding_id int,
	area_key int,
	value float8
)

create table tmp_total_dbt_staff_each_area_and_month
(
	month_key int,
	area_key int,
	total_debt_aft_wo_grp1 float8,
	total_debt_aft_wo_grp2 float8,
	total_debt_aft_wo_grp2_5 float8,
	total_debt_aft_wo float8,
	total_wo float8,
	total_wo_next_month float8
)

drop table tmp_total_dbt_staff_each_area_and_month

create table tmp_total_dist_debt_staff_monthly
(
	month_key int,
	area_key int,
	debt_aft_wo float8,
	debt_aft_wo_grp1 float8,
	debt_aft_wo_grp2 float8,
	debt_aft_wo_grp2345 float8,
	debt_bef_wo_grp2345 float8,
	psdn float8,
	amount_sm float8,
	npl_grp345 float8,
	cum_wo float8,
	debt_aft_wo_month float8
)

drop table tmp_total_dist_debt_staff_monthly

create table tmp_ratio_each_area_to_all_area
(
	month_key int,
	area_key int,
	ratio_debt_aft_wo_grp1 float,
	ratio_debt_aft_wo_grp2 float,
	ratio_debt_aft_wo_grp2345 float,
	ratio_bef_aft_wo_grp2345 float,
	ratio_psdn float,
	ratio_sm float,
	ratio_debt_aft_wo float
)

create table fact_summary_report_monthly
(
	month_key int,
	area_key int,
	report_id int,
	amt_dist_ytm_from_gl float8,
	amt_dist_ytm_from_gl_final float8
)

create table dim_funding_structure
(
	funding_id int,
	funding_code varchar,
	funding_name varchar,
	funding_parent_id int,
	funding_level int,
	sortorder int,
	rec_created_dt timestamp default now(),
	rec_updated_dt timestamp default now()
)

create table asm_rank_report 
	(
		month_key int,
		area_cde varchar,
		area_name varchar,
		email varchar,
		final_score int,
		rank_final int,
		ltn_avg float8,
		rank_ltn int,
		psdn_avg float8,
		rank_psdn int,
		approval_rate_avg float,
		rank_approval_rate int,
		npl_truoc_wo_luy_ke float,
		rank_npl_truoc_wo_luy_ke int,
		scale_score int,
		rank_ptkd int,
		cir float8,
		rank_cir int,
		margin float8,
		rank_margin int,
		hs_von float8,
		rank_hs_von int,
		hsbq_nhan_su float8,
		rank_hsbq_nhan_su int,
		fin_score int,
		rank_fin int
	)

drop table dim_funding_structure

insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (1, 'PBT', '1. Lợi nhuận trước thuế', -1, 0, 1000000);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (7, 'PBT01001', 'Thu nhập từ hoạt động thẻ', 2, 2, 1010000);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (10, 'PBT010010001', 'Lãi trong hạn', 3, 3, 1010100);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (11, 'PBT010010002', 'Lãi quá hạn', 3, 3, 1010101);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (12, 'PBT010010003', 'Phí bảo hiểm', 3, 3, 1010102);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (13, 'PBT010010004', 'Phí tăng hạn mức', 3, 3, 1010103);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (14, 'PBT010010005', 'Phí thanh toán chậm, thu từ ngoại bảng, khác,…', 3, 3, 1010104);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (8, 'PBT01002', 'Chi phí thuần KDV', 2, 2, 1020000);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (15, 'PBT010020001', 'CP vốn TT2', 4, 3, 1020100);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (16, 'PBT010020002', 'CP vốn CCTG', 4, 3, 1020101);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (9, 'PBT01003', 'Chi phí thuần hoạt động khác', 2, 2, 1030000);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (17, 'PBT010030001', 'DT Kinh doanh', 5, 3, 1030100);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (18, 'PBT010030002', 'CP hoa hồng', 5, 3, 1030101);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (19, 'PBT010030003', 'CP thuần KD khác', 5, 3, 1030102);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (4, 'PBT01', 'Tổng thu nhập hoạt động', 1, 1, 1040000);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (5, 'PBT02', 'Tổng chi phí hoạt động', 1, 1, 1050000);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (20, 'PBT02001', 'CP nhân viên', 6, 2, 1050100);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (21, 'PBT02002', 'CP quản lý', 6, 2, 1050101);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (22, 'PBT02003', 'CP tài sản', 6, 2, 1050102);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (6, 'PBT03', 'Chi phí dự phòng', 1, 1, 1060000);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (2, 'SM', '2. Số lượng nhân sự (Sale Manager)', -1, 0, 2000000);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (3, 'FR', '3. Chỉ số tài chính', -1, 0, 3000000);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (23, 'FR01', 'CIR (%)', 7, 1, 3010100);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (24, 'FR02', 'Margin (%)', 7, 1, 3010101);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (25, 'FR03', 'Hiệu suất trên/vốn (%)', 7, 1, 3010102);insert into dim_funding_structure (funding_id, funding_code, funding_name, funding_parent_id, funding_level, sortorder)
values (26, 'FR04', 'Hiệu suất BQ/ Nhân sự', 7, 1, 3010103);

select *
from dim_funding_structure 

create table dim_area
(
	area_id int,
	area_code varchar,
	area_name varchar,
	rec_created_dt timestamp default now(),
	rec_updated_dt timestamp default now()
)

drop table dim_area 

insert into dim_area (area_id, area_code, area_name)
values 
	(0, 'A', 'Hội Sở'),
	(1, 'B', 'Đông Bắc Bộ'),
	(2, 'C', 'Tây Bắc Bộ'),
	(3, 'D', 'Đồng Bằng Sông Hồng'),
	(4, 'E', 'Bắc Trung Bộ'),
	(5, 'F', 'Nam Trung Bộ'),
	(6, 'G', 'Tây Nam Bộ'),
	(7, 'H', 'Đông Nam Bộ');

select *
from dim_area 

select distinct transaction_date 
from fact_txn_month_raw_data ftmrd 

create table dim_date
(
	date_id date primary key,
	day int,
	month int,
	year int,
	quarter int,
	month_key int,
	rec_created_dt timestamp default now(),
	rec_updated_dt timestamp default now()
)

drop table dim_date 

insert into dim_date (date_id)
values 
	('2023-01-31'::date),
	('2023-02-28'::date),
	('2023-03-31'::date),
	('2023-04-30'::date),
	('2023-05-31'::date)
	
update dim_date 
set day = extract(day from date_id),
	month = extract(month from date_id),
	year = extract(year from date_id),
	quarter = extract(quarter from date_id),
	month_key = to_char(date_id, 'YYYYMM')::INT,
	rec_updated_dt = now()

CREATE SEQUENCE city_id_seq
    START WITH 0
    MINVALUE 0
    INCREMENT BY 1;

	
create table dim_city
(
	city_id INT PRIMARY KEY DEFAULT nextval('city_id_seq'),
	city_name varchar,
	area_key int,
	rec_created_dt timestamp default now(),
	rec_updated_dt timestamp default now()
)

drop SEQUENCE city_id_seq 

insert into dim_city (city_name, area_key) 
values 
	('Bắc Giang', 1),
    ('Bắc Kạn', 1),
    ('Cao Bằng', 1),
    ('Hà Giang', 1),
    ('Lạng Sơn', 1),
    ('Phú Thọ', 1),
    ('Quảng Ninh', 1),
    ('Thái Nguyên', 1),
    ('Tuyên Quang', 1),
    ('Điện Biên', 2),
    ('Hòa Bình', 2),
    ('Lai Châu', 2),
    ('Lào Cai', 2),
    ('Sơn La', 2),
    ('Yên Bái', 2),
    ('Bắc Ninh', 3),
    ('Hà Nam', 3),
    ('Hà Nội', 3),
    ('Hải Dương', 3),
    ('Hải Phòng', 3),
    ('Hưng Yên', 3),
    ('Nam Định', 3),
    ('Ninh Bình', 3),
    ('Thái Bình', 3),
    ('Vĩnh Phúc', 3),
    ('Hà Tĩnh', 4),
    ('Huế', 4),
    ('Nghệ An', 4),
    ('Quảng Bình', 4),
    ('Quảng Trị', 4),
    ('Thanh Hóa', 4),
    ('Bình Định', 5),
    ('Bình Thuận', 5),
    ('Đà Nẵng', 5),
    ('Đắk Lắk', 5),
    ('Đắk Nông', 5),
    ('Gia Lai', 5),
    ('Khánh Hòa', 5),
    ('Kon Tum', 5),
    ('Lâm Đồng', 5),
    ('Ninh Thuận', 5),
    ('Phú Yên', 5),
    ('Quảng Nam', 5),
    ('Quảng Ngãi', 5),
     ('Cần Thơ', 6),
    ('Đồng Tháp', 6),
    ('Hậu Giang', 6),
    ('Kiên Giang', 6),
    ('Long An', 6),
    ('Sóc Trăng', 6),
    ('Tiền Giang', 6),
    ('Trà Vinh', 6),
    ('Vĩnh Long', 6),
    ('An Giang', 6),
    ('Bạc Liêu', 6),
    ('Bến Tre', 6),
    ('Cà Mau', 6),
    ('Bà Rịa - Vũng Tàu', 7),
    ('Bình Dương', 7),
    ('Bình Phước', 7),
    ('Đồng Nai', 7),
    ('Hồ Chí Minh', 7),
    ('Tây Ninh', 7);
    
select *
from dim_city dc 

CREATE TABLE procedure_log (
    id SERIAL PRIMARY KEY,
    procedure_name VARCHAR(255) NOT NULL,
    log_message TEXT NOT NULL,
    log_level VARCHAR(50) NOT NULL,
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select *
from procedure_log 

create table dim_staff
(
	sm_id serial primary key,
	sm_name varchar,
	sm_email varchar,
	area_key int,
	rec_created_dt timestamp default now(),
	rec_updated_dt timestamp default now()
)



select *
from dim_funding_structure 

select *
from dim_area 
