create or replace procedure prc_processing_raw_data(
	-- Bổ sung các tham số nếu cần
)
as $$ 
declare 
begin 
	
	-- ---------------------
    -- THÔNG TIN NGƯỜI TẠO
    -- ---------------------
    -- Tên người tạo: Đoàn Hoài Việt
    -- Ngày tạo: 2025-04-07
    -- Mục đích : Biến đổi ngày tháng, thêm funding_id và xóa bỏ các cột không cần thiết

    -- ---------------------
    -- THÔNG TIN NGƯỜI CẬP NHẬT
    -- ---------------------
    -- Tên người cập nhật: Đoàn Hoài Việt
    -- Ngày cập nhật: 2025-05-31
    -- Mục đích cập nhật: Thêm xử lý data cho bảng fact_kpi, bảng kpi_asm

    -- ---------------------
    -- SUMMARY LUỒNG XỬ LÝ
    -- ---------------------
    -- Bước 1: Kiểm tra nếu fact_txn đã tồn tại thì xóa đi
    -- Bước 2: Tạo bảng fact_txn mới với dữ liệu đã được thay đổi
	-- Bước 3: Ghép 3 sheet của file kpi raw data lại
	-- Bước 4: Kiểm tra nếu fact_kpi đã tồn tại thì xóa đi
	-- Bước 5: Tạo bảng fact_kpi mới với việc thêm cột mã vùng
	-- Bước 6: Kiểm tra nếu kpi_asm đã tồn tại thì xóa đi
	-- Bước 7: Tạo bảng kpi_asm mới với việc thêm cột mã vùng
	
	-----------------------
	-- CHI TIẾT CÁC BƯỚC
	-----------------------
	
	-- Bước 1: Kiểm tra nếu đã tồn tại bảng thì xóa đi
	DROP TABLE IF EXISTS fact_txn;

	-- Bước 2: Tạo bảng mới với dữ liệu đã được thay đổi
	create table fact_txn as
	select to_char(transaction_date, 'YYYYMM')::int + 200 as month_key, account_code, amount, 
		case 
			when substring(analysis_code from 9 for 1) = '0' then 'A'
			else substring(analysis_code from 9 for 1)
		end as area_key,
		case
			when account_code in (702000030002, 702000030001,702000030102) then 10
			when account_code in (702000030012, 702000030112) then 11
			when account_code = 716000000001 then 12
			when account_code = 719000030002 then 13
			when account_code in (719000030003,719000030103,790000030003,790000030103,790000030004,790000030104) then 14
			when account_code = 803000000001 then 16
			when account_code in (801000000001,802000000001) then 15
			when account_code in (816000000001,816000000002,816000000003) then 18
			when account_code in (809000000002,809000000001,811000000001,811000000102,811000000002,811014000001,811037000001,811039000001,811041000001,815000000001,819000000002,819000000003,819000000001,790000000003,790000050101,790000000101,790037000001,849000000001,899000000003,899000000002,811000000101,819000060001) then 19
			when account_code in (702000010001,702000010002,704000000001,705000000001,709000000001,714000000002,714000000003,714037000001,714000000004,714014000001,715000000001,715037000001,719000000001,709000000101,719000000101) then 17
			when account_code::text like '85%' then 20
			when account_code::text like '86%' then 21
			when account_code::text like '87%' then 22
			when account_code in (790000050001, 882200050001, 790000030001, 882200030001, 790000000001, 790000020101, 882200000001, 882200050101, 882200020101, 882200060001,790000050101,882200030101) then 6
			else -1
		end funding_id 
	from fact_txn_month_raw_data;

	-- Đầu tiên, cập nhật dữ liệu với giá trị từ dim_area
	UPDATE fact_txn f
	SET area_key = (SELECT area_id FROM dim_area d WHERE f.area_key = d.area_code);

	-- Sau đó chuyển đổi kiểu dữ liệu của cột
	ALTER TABLE fact_txn ALTER COLUMN area_key TYPE INTEGER USING area_key::INTEGER;

	-- Bước 3: Ghép 3 sheet của file kpi raw data lại
	drop table if exists fact_kpi_month_raw_data;
	create table fact_kpi_month_raw_data as
	select * 
	from fact_kpi_month_raw_data_sheet0
	union all
	select * 
	from fact_kpi_month_raw_data_sheet1
	union all 
	select *
	from fact_kpi_month_raw_data_sheet2;
	-- Bước 4: Kiểm tra nếu đã tồn tại bảng thì xóa đi
	drop table if exists fact_kpi;

	-- Bước 5: Tạo bảng fact_kpi mới với việc thêm cột mã vùng
	create table fact_kpi as
	select kpi_month + 200 as month_key, pos_cde, pos_city, application_id, outstanding_principal, write_off_month + 200 as write_off_month, write_off_balance_principal, psdn, coalesce(max_bucket, 1) as max_bucket, 
		case
			when pos_city in ('Bắc Giang', 'Bắc Kạn', 'Cao Bằng', 'Hà Giang', 'Lạng Sơn', 'Phú Thọ', 'Quảng Ninh', 'Thái Nguyên', 'Tuyên Quang') then 1
			when pos_city in ('Điện Biên', 'Hòa Bình', 'Lai Châu', 'Lào Cai', 'Sơn La', 'Yên Bái') then 2
			when pos_city in ('Bắc Ninh', 'Hà Nam', 'Hà Nội', 'Hải Dương', 'Hải Phòng', 'Hưng Yên', 'Nam Định', 'Ninh Bình', 'Thái Bình', 'Vĩnh Phúc') then 3
			when pos_city in ('Hà Tĩnh', 'Huế', 'Nghệ An', 'Quảng Bình', 'Quảng Trị', 'Thanh Hóa') then 4
			when pos_city in ('Bình Định', 'Bình Thuận', 'Đà Nẵng', 'Đắk Lắk', 'Đắk Nông', 'Gia Lai', 'Khánh Hòa', 'Kon Tum', 'Lâm Đồng', 'Ninh Thuận', 'Phú Yên', 'Quảng Nam', 'Quảng Ngãi') then 5
			when pos_city in ('Cần Thơ', 'Đồng Tháp', 'Hậu Giang', 'Kiên Giang', 'Long An', 'Sóc Trăng', 'Tiền Giang', 'Trà Vinh', 'Vĩnh Long', 'An Giang', 'Bạc Liêu', 'Bến Tre', 'Cà Mau') then 6
			when pos_city in ('Bà Rịa - Vũng Tàu', 'Bình Dương', 'Bình Phước', 'Đồng Nai', 'Hồ Chí Minh', 'Tây Ninh') then 7
		end as area_key
	from fact_kpi_month_raw_data;

	-- Bước 6: Kiểm tra nếu đã tồn tại bảng thì xóa đi
	drop table if exists kpi_asm;

	-- Bước 7: Tạo bảng kpi_asm mới với việc thêm cột mã vùng
	create table kpi_asm as 
	select *, 
		case 
			when area_name = 'Đông Bắc Bộ' then 1
			when area_name = 'Tây Bắc Bộ' then 2
			when area_name = 'Đồng Bằng Sông Hồng' then 3
			when area_name = 'Bắc Trung Bộ' then 4
			when area_name = 'Nam Trung Bộ' then 5
			when area_name = 'Tây Nam Bộ' then 6
			when area_name = 'Đông Nam Bộ' then 7
		end as area_key 
	from kpi_asm_data k;

	update kpi_asm 
	set month_key = month_key + 200;
	
end;
$$ language plpgsql;

call prc_processing_raw_data();

create or replace procedure fct_summary_report_asm_ranked_monthly_prc(
	-- Bổ sung thêm các tham số nếu cần
	p_date date default NULL
)
as $$
declare 
	-- Bổ sung các biến nếu cần
	vProcess_Month int;	
	prc_name varchar := 'fct_summary_report_asm_ranked_monthly_prc';
			
begin
	
	-- ---------------------
    -- THÔNG TIN NGƯỜI TẠO
    -- ---------------------
    -- Tên người tạo: Đoàn Hoài Việt
    -- Ngày tạo: 2025-03-16
    -- Mục đích : In ra 2 mẫu báo cáo tổng hợp hợp và báo cáo xếp hạng 

    -- ---------------------
    -- THÔNG TIN NGƯỜI CẬP NHẬT
    -- ---------------------
    -- Tên người cập nhật: 
    -- Ngày cập nhật: 
    -- Mục đích cập nhật: 

    -- ---------------------
    -- SUMMARY LUỒNG XỬ LÝ
    -- ---------------------
	-- Bước 1: Gọi prc_processing_raw_data để xử lý dữ liệu
    -- Bước 2: Kiểm tra nếu tháng truyền vào là null thì sẽ lấy tháng hiện tại - 1
        -- ngược lại vProcess_Month = vMonth
    -- Bước 3: Xóa dữ liệu tại bảng fact_summary_report_monthly tại tháng vProcess_Month 
    -- Bước 4: Insert dữ liệu phân bổ từng hạng mục vào bảng fact_summary_report_monthly
	-- Bước 5: Xóa dữ liệu tại bảng asm_rank_report
    -- Bước 6: insert dữ liệu xếp hạng nhân viên vào bảng asm_rank_report
    -- Bước 7: Xử lý ngoại lệ và ghi log (nếu cần)

    -- ---------------------
    -- CHI TIẾT CÁC BƯỚC
    -- ---------------------
	
	-- Bước 1: Gọi prc_processing_raw_data để xử lý dữ liệu
	
	
	-- Bước 2: Kiểm tra tháng truyền vào, nếu là null thì mặc định là tháng hiện tại nếu ko thì giữ nguyên
	if p_date is null then
		vProcess_Month := to_char(now(), 'YYYYMM')::int;
	else 
		vProcess_Month = to_char(p_date, 'YYYYMM')::int;
	end if;

	-- Bước 3: Xóa dữ liệu tại bảng fact_summary_funding_month tại tháng vProcess_Month 
	delete  from fact_summary_report_monthly where month_key = vProcess_Month;

	-- 3.1: Insert dữ liệu vào bảng tmp_report_gl_by_area_monthly
	-- Xóa dữ liệu tại vProcess_Month 
	delete from tmp_report_gl_by_area_monthly where month_key = vProcess_Month;

	-- Insert dữ liệu
	insert into tmp_report_gl_by_area_monthly
	select vProcess_Month, funding_id, area_key, sum(amount) 
	from fact_txn 
	where month_key <= vProcess_Month and funding_id > 0
	group by funding_id, area_key;

	-- 3.2: Insert dữ liệu vào bảng tmp_total_dbt_staff_each_area_and_month 
	-- Xóa dữ liệu tại thời điểm bé hơn hoặc bằng vProcess_Month 
	DELETE FROM tmp_total_dbt_staff_each_area_and_month WHERE month_key <= vProcess_Month;
	-- Insert dư

	insert into tmp_total_dbt_staff_each_area_and_month
	select a.month_key, a.area_key, total_debt_aft_wo_grp1, total_debt_aft_wo_grp2, total_debt_aft_wo_grp2_5, total_debt_aft_wo, total_wo, total_wo_next
	from 
	(
		-- dư nợ nhóm 1 (bucket 1)
		SELECT month_key, area_key, SUM(outstanding_principal) AS total_debt_aft_wo_grp1
		FROM fact_kpi
		WHERE month_key <= vProcess_Month AND max_bucket = 1  
		GROUP BY month_key, area_key  
	) a
	join 
	(
		-- dư nợ nhóm 2 (bucket 2)
	    SELECT month_key, area_key, SUM(outstanding_principal) AS total_debt_aft_wo_grp2
	    FROM fact_kpi
	    WHERE month_key <= vProcess_Month  AND max_bucket = 2
	    GROUP BY month_key, area_key 
	) b on a.month_key = b.month_key and a.area_key = b.area_key 
	join
	(
		-- dư nợ nhóm 2,3,4,5 (bucket 2-5)
	    SELECT month_key, area_key, SUM(outstanding_principal) AS total_debt_aft_wo_grp2_5
	    FROM fact_kpi
	    WHERE month_key <= vProcess_Month AND max_bucket BETWEEN 2 AND 5
	    GROUP BY month_key, area_key 
	) c on b.month_key = c.month_key and b.area_key = c.area_key 
	join 
	(
		-- dư nợ tất cả các nhóm (bucket 1-5)
	    SELECT month_key, area_key, SUM(outstanding_principal) AS total_debt_aft_wo
	    FROM fact_kpi
	    WHERE month_key <= vProcess_Month 
	    GROUP BY month_key, area_key 
	) d on c.month_key = d.month_key and c.area_key = d.area_key  
	join
	(
		-- write-off theo tháng và khu vực
	    SELECT 
	        month_key, 
	        area_key, 
	        SUM(write_off_balance_principal) AS total_wo,
	        LEAD(SUM(write_off_balance_principal), 1, 0) OVER (PARTITION BY area_key ORDER BY write_off_month DESC) AS total_wo_next
	    FROM fact_kpi
	    WHERE month_key <= vProcess_Month AND write_off_month = month_key
	    GROUP BY month_key, write_off_month, area_key 
	) e on d.month_key = e.month_key and d.area_key = e.area_key;

	-- 3.3: Chèn dữ liệu vào bảng tmp_total_dist_debt_staff_monthly
	-- Xóa dữ liệu tại thời điểm vProcess_Month 
	delete from tmp_total_dist_debt_staff_monthly where vProcess_Month = month_key;

	INSERT INTO tmp_total_dist_debt_staff_monthly
	SELECT vProcess_Month, 0, avg_dbt_aft, avg_dbt_aft_grp1, avg_dbt_aft_grp2, avg_dbt_aft_grp2345, total_dbt_bef_grp2345, allpsdn, allsm, total_debt_aft_wo_cur_month, sum_wo_vung, sum_no_vung
	from 
	(
		-- Tổng dư nợ cuối kỳ bình quân toàn khu vực nhóm 1,2,3,4,5
	    select avg(total_dbt_aft) as avg_dbt_aft
		from 
		(
			SELECT SUM(total_debt_aft_wo) as total_dbt_aft 
		    FROM tmp_total_dbt_staff_each_area_and_month
		    where month_key <= vProcess_Month 
		    group by month_key 
		)
	) a
	join 
	(
		-- Tổng dư nợ cuối kỳ bình quân toàn khu vực nhóm 1
		select avg(total_dbt_aft_grp1) as avg_dbt_aft_grp1
		from 
		(
			SELECT SUM(total_debt_aft_wo_grp1) as total_dbt_aft_grp1
		    FROM tmp_total_dbt_staff_each_area_and_month
		    where month_key <= vProcess_Month  
		    group by month_key 
		)
	) b on 1 = 1
	join 
	(
		-- Tổng dư nợ cuối kỳ bình quân toàn khu vực nhóm 2
		select avg(total_dbt_aft_grp2) as avg_dbt_aft_grp2
		from 
		(
			SELECT SUM(total_debt_aft_wo_grp2) as total_dbt_aft_grp2
		    FROM tmp_total_dbt_staff_each_area_and_month
		    where month_key <= vProcess_Month  
		    group by month_key 
		)
	) c on 1 = 1
	join 
	(
		-- Tổng dư nợ cuối kỳ bình quân toàn khu vực nhóm 2,3,4,5
	 	select avg(total_dbt_aft_grp2345) as avg_dbt_aft_grp2345
		from 
		(
			SELECT SUM(total_debt_aft_wo_grp2_5) as total_dbt_aft_grp2345
		    FROM tmp_total_dbt_staff_each_area_and_month
		    where month_key <= vProcess_Month  
		    group by month_key 
		)
	) d on 1 = 1
	join 
	(
		-- Số dư cuối kỳ lũy kế của toàn khu vực trước wo nhóm 2,3,4,5
		SELECT SUM(total_debt_aft_wo_grp2_5 + total_wo + total_wo_next_month) as total_dbt_bef_grp2345
		FROM tmp_total_dbt_staff_each_area_and_month 
		where month_key <= vProcess_Month  
	) e on 1 = 1
	join 
	(
		-- Tổng thẻ PSDN
		select count(psdn) as allpsdn 
		from fact_kpi 
		where month_key <= vProcess_Month  
	) f on 1 = 1
	join 
	(
		-- Tổng số lượng SM
		select count(*) as allsm
		from dim_staff ds 
	) g on 1 = 1
	join 
	(
		-- Tổng npl tại tất cả vùng
		select sum(outstanding_principal) as total_debt_aft_wo_cur_month
		from fact_kpi
		where month_key = vProcess_Month
		and max_bucket in (3,4,5)
	) h on 1 = 1
	join 
	(
		-- Lũy kế WO tất cả vùng 
		select sum(write_off_balance_principal) as sum_wo_vung 
		from fact_kpi
		where month_key <= vProcess_Month and write_off_month = month_key  
	) j on 1 = 1
	join 
	(
		-- tổng dư nợ của toàn vùng tại vProcess_Month 
		select sum(outstanding_principal) as sum_no_vung 
		from fact_kpi
		where month_key = vProcess_Month  
	) i on 1 = 1
	union all
	SELECT vProcess_Month, a.area_key, avg_dbt_aft, avg_dbt_aft_grp1, avg_dbt_aft_grp2, avg_dbt_aft_grp2345, total_dbt_bef_grp2345, allpsdn, allsm, total_debt_aft_wo_cur_month, sum_wo_vung, sum_no_vung
	from 
	(
		-- Tổng dư nợ cuối kỳ bình quân từng khu vực nhóm 1,2,3,4,5
	    select area_key, avg(total_dbt_aft) as avg_dbt_aft
		from 
		(
			select area_key, SUM(total_debt_aft_wo) as total_dbt_aft 
		    FROM tmp_total_dbt_staff_each_area_and_month
		    where month_key <= vProcess_Month 
		    group by month_key, area_key  
		)
		group by area_key
	) a
	join 
	(
		-- Tổng dư nợ cuối kỳ bình quân từng khu vực nhóm 1
		select area_key, avg(total_dbt_aft_grp1) as avg_dbt_aft_grp1
		from 
		(
			SELECT area_key, SUM(total_debt_aft_wo_grp1) as total_dbt_aft_grp1
		    FROM tmp_total_dbt_staff_each_area_and_month
		    where month_key <= vProcess_Month  
		    group by month_key, area_key  
		)
		group by area_key
	) b on a.area_key = b.area_key 
	join 
	(
		-- Tổng dư nợ cuối kỳ bình quân từng khu vực nhóm 2
		select area_key, avg(total_dbt_aft_grp2) as avg_dbt_aft_grp2
		from 
		(
			SELECT area_key, SUM(total_debt_aft_wo_grp2) as total_dbt_aft_grp2
		    FROM tmp_total_dbt_staff_each_area_and_month
		    where month_key <= vProcess_Month  
		    group by month_key, area_key  
		)
		group by area_key 
	) c on b.area_key = c.area_key 
	join 
	(
		-- Tổng dư nợ cuối kỳ bình quân từng khu vực nhóm 2,3,4,5
	 	select area_key, avg(total_dbt_aft_grp2345) as avg_dbt_aft_grp2345
		from 
		(
			SELECT area_key, SUM(total_debt_aft_wo_grp2_5) as total_dbt_aft_grp2345
		    FROM tmp_total_dbt_staff_each_area_and_month
		    where month_key <= vProcess_Month  
		    group by month_key, area_key 
		)
		group by area_key 
	) d on c.area_key = d.area_key 
	join 
	(
		-- Số dư cuối kỳ lũy kế của từng khu vực trước wo nhóm 2,3,4,5
		SELECT area_key, SUM(total_debt_aft_wo_grp2_5 + total_wo + total_wo_next_month) as total_dbt_bef_grp2345
		FROM tmp_total_dbt_staff_each_area_and_month 
		where month_key <= vProcess_Month 
		group by area_key 
	) e on d.area_key = e.area_key 
	join 
	(
		-- Tổng thẻ PSDN từng vùng
		select area_key, count(psdn) as allpsdn 
		from fact_kpi 
		where month_key <= vProcess_Month  
		group by area_key 
	) f on e.area_key = f.area_key 
	join 
	(
		-- Tổng số lượng SM từng vùng
		select area_id, count(*) as allsm
		from dim_staff ds 
		join dim_area da on da.area_id = ds.area_key  
		group by area_id 
	) g on f.area_key = g.area_id
	join 
	(
		-- Tổng npl tại từng vùng
		select area_key, sum(outstanding_principal) as total_debt_aft_wo_cur_month
		from fact_kpi
		where month_key = vProcess_Month and max_bucket in (3,4,5)
		group by area_key 
	) h on g.area_id = h.area_key 
	join 
	(
		-- Lũy kế WO từng vùng 
		select area_key, sum(write_off_balance_principal) as sum_wo_vung 
		from fact_kpi
		where month_key <= vProcess_Month and write_off_month = month_key  
		group by area_key 
	) j on h.area_key = j.area_key 
	join 
	(
		-- tổng dư nợ của từng vùng tại vProcess_Month 
		select area_key, sum(outstanding_principal) as sum_no_vung 
		from fact_kpi
		where month_key = vProcess_Month
		group by area_key 
	) i on j.area_key = i.area_key;
	
	-- 3.4: Chèn dữ liệu vào bảng tmp_ratio_each_area_to_all_area
	-- Xóa dữ liệu tại bảng tmp_ratio_each_area_to_all_area
	delete from tmp_ratio_each_area_to_all_area where month_key = vProcess_Month;

	-- Insert dữ liệu
	insert into tmp_ratio_each_area_to_all_area 
	select t1.month_key, t1.area_key, 
		t1.debt_aft_wo_grp1::float / t2.debt_aft_wo_grp1 as ratio_debt_aft_wo_grp1,
		t1.debt_aft_wo_grp2::float / t2.debt_aft_wo_grp2 as ratio_debt_aft_wo_grp2,
		t1.debt_aft_wo_grp2345::float / t2.debt_aft_wo_grp2345 as ratio_debt_aft_wo_grp2345,
		t1.debt_bef_wo_grp2345::float / t2.debt_bef_wo_grp2345 as ratio_bef_aft_wo_grp2345,
		t1.psdn / t2.psdn::float as ratio_psdn,
		t1.amount_sm::float / t2.amount_sm as ratio_sm,
		t1.debt_aft_wo / t2.debt_aft_wo as ratio_debt_aft_wo
	from tmp_total_dist_debt_staff_monthly t1
	join tmp_total_dist_debt_staff_monthly t2 on t1.month_key = t2.month_key and t2.area_key = 0
	where t1.month_key = vProcess_Month;

	update tmp_ratio_each_area_to_all_area 
	set ratio_debt_aft_wo_grp1 = 0,
		ratio_debt_aft_wo_grp2 = 0,
		ratio_debt_aft_wo_grp2345 = 0,
		ratio_bef_aft_wo_grp2345 = 0,
		ratio_psdn = 0,
		ratio_sm = 0,
		ratio_debt_aft_wo = 0
	where area_key = 0;

	-- 3.5: Insert dữ liệu vào bảng fact_summary_report_monthly 
	-- Xóa dữ liệu 
	delete from fact_summary_report_monthly where month_key = vProcess_Month;

	-- Insert dữ liệu
	insert into fact_summary_report_monthly  
	select vProcess_Month, t1.area_key, t1.funding_id, t1.amt_dist_ytm_from_gl,
		case 
			WHEN t1.funding_id IN (10, 13) THEN t1.amt_dist_ytm_from_gl + ratio_debt_aft_wo_grp1 * t2.amt_dist_ytm_from_gl -- Lãi trong hạn, phí tăng hạn mức
	        WHEN t1.funding_id = 11 THEN t1.amt_dist_ytm_from_gl + ratio_debt_aft_wo_grp2 * t2.amt_dist_ytm_from_gl -- Lãi quá hạn
	        WHEN t1.funding_id = 12 THEN t1.amt_dist_ytm_from_gl + ratio_psdn * t2.amt_dist_ytm_from_gl -- Phí bảo hiểm
	        WHEN t1.funding_id = 14 THEN t1.amt_dist_ytm_from_gl + ratio_bef_aft_wo_grp2345 * t2.amt_dist_ytm_from_gl -- Phí thanh toán chậm, thu từ ngoại bảng, khác...
	        WHEN t1.funding_id IN (17, 18, 19) THEN t1.amt_dist_ytm_from_gl + ratio_debt_aft_wo * t2.amt_dist_ytm_from_gl -- DT kinh doanh, CP hoa hồng, CP thuần KD khác
	        WHEN t1.funding_id IN (20, 21, 22) THEN t1.amt_dist_ytm_from_gl + ratio_sm * t2.amt_dist_ytm_from_gl -- CP nhân viên, quản lý, tài sản
	        WHEN t1.funding_id = 6 THEN t1.amt_dist_ytm_from_gl + ratio_bef_aft_wo_grp2345 * t2.amt_dist_ytm_from_gl -- CP dự phòng rủi ro
		end as amt_dist_ytm_from_gl_final
	from tmp_report_gl_by_area_monthly t1
	join tmp_report_gl_by_area_monthly t2 on t1.month_key = t2.month_key and t2.area_key = 0 and t1.funding_id = t2.funding_id 
	join tmp_ratio_each_area_to_all_area tr on t1.month_key = tr.month_key and t1.area_key = tr.area_key 
	where t1.month_key = vProcess_Month and t1.funding_id not in (15, 16)
	union all
	select vProcess_Month, tr.area_key, funding_id, amt_dist_ytm_from_gl, -- CP vốn TT2, CP vốn CCTG
		case
			when amt_dist_ytm_from_gl * ratio_debt_aft_wo  = 0 then amt_dist_ytm_from_gl 
			else amt_dist_ytm_from_gl * ratio_debt_aft_wo 
		end as amt_dist_ytm_from_gl_final
	from tmp_report_gl_by_area_monthly t1
	join tmp_ratio_each_area_to_all_area tr on 1 = 1 and t1.month_key = tr.month_key 
	where funding_id in (15, 16) and t1.month_key = vProcess_Month;
	
	insert into fact_summary_report_monthly  
	select vProcess_Month, area_key, 
		case 
			when funding_parent_id = 3 then 7 -- Thu nhập từ hoạt động thẻ 
			when funding_parent_id = 4 then 8 -- Chi phí thuần KDV 
			when funding_parent_id = 5 then 9 -- Chi phí thuần hoạt động khác
			when funding_parent_id = 6 then 5 -- Tổng chi phí hoạt động
		end as report_id, 
		sum(amt_dist_ytm_from_gl), sum(amt_dist_ytm_from_gl_final) as amt_dist_ytm_from_gl_final 
	from fact_summary_report_monthly f 
	join dim_funding_structure d on f.report_id = d.funding_id 
	where month_key = vProcess_Month and f.report_id <> 6
	group by funding_parent_id, area_key;
	
	insert into fact_summary_report_monthly
	select vProcess_Month, area_key, 4, sum(amt_dist_ytm_from_gl), sum(amt_dist_ytm_from_gl_final) -- Tổng thu nhập hoạt động
	from fact_summary_report_monthly f
	join dim_funding_structure d on f.report_id = d.funding_id 
	where month_key = vProcess_Month and funding_parent_id = 2
	group by area_key;

	insert into fact_summary_report_monthly
	select vProcess_Month, area_key, 1, sum(amt_dist_ytm_from_gl), sum(amt_dist_ytm_from_gl_final) -- Lợi nhuận trước thuế
	from fact_summary_report_monthly f
	join dim_funding_structure d on f.report_id = d.funding_id 
	where month_key = vProcess_Month and funding_parent_id = 1
	group by area_key
 	union all
 	select vprocess_month, area_key, 2, amount_sm, amount_sm -- Số lượng SM
	from tmp_total_dist_debt_staff_monthly 
	where month_key = vprocess_month;

	insert into fact_summary_report_monthly
	select vprocess_month, t1.area_key, 23, -t1.amt_dist_ytm_from_gl / t2.amt_dist_ytm_from_gl * 100, -t1.amt_dist_ytm_from_gl_final / t2.amt_dist_ytm_from_gl_final * 100 -- CIR%
	from 
		fact_summary_report_monthly t1 
	join 	
		fact_summary_report_monthly t2 
		on t1.report_id = 5 
		and t2.report_id = 4 
		and t1.area_key = t2.area_key 
		and t1.month_key = t2.month_key 
	where t1.month_key = vprocess_month 
	union all
	select vprocess_month, t1.area_key, 24, t1.amt_dist_ytm_from_gl / (t2.amt_dist_ytm_from_gl + t3.amt_dist_ytm_from_gl) * 100, t1.amt_dist_ytm_from_gl_final / (t2.amt_dist_ytm_from_gl_final + t3.amt_dist_ytm_from_gl_final) * 100 -- Margin%
	from
		fact_summary_report_monthly t1 
	join 	
		fact_summary_report_monthly t2 
		on t1.report_id = 1 
		and t2.report_id = 7
		and t1.area_key = t2.area_key
		and t1.month_key = t2.month_key 
	join 	
		fact_summary_report_monthly t3
		on t3.report_id = 17 
		and t1.area_key = t3.area_key
		and t1.month_key = t3.month_key 
	where t1.month_key = vprocess_month 
	union all
	select vprocess_month, t1.area_key, 25, -t1.amt_dist_ytm_from_gl / t2.amt_dist_ytm_from_gl * 100, -t1.amt_dist_ytm_from_gl_final / t2.amt_dist_ytm_from_gl_final * 100 -- Hiệu suất trên vốn bình quân%
	from 
		fact_summary_report_monthly t1 
	join 	
		fact_summary_report_monthly t2 
		on t1.report_id = 1 
		and t2.report_id = 8
		and t1.area_key = t2.area_key 
		and t1.month_key = t2.month_key 
	where t1.month_key = vprocess_month 
	union all
	select vprocess_month, t1.area_key, 26, t1.amt_dist_ytm_from_gl / t2.amt_dist_ytm_from_gl * 100, t1.amt_dist_ytm_from_gl_final / t2.amt_dist_ytm_from_gl_final * 100 -- Hiệu suất BQ/Nhân sự
	from 
		fact_summary_report_monthly t1 
	join 	
		fact_summary_report_monthly t2 
		on t1.report_id = 1 
		and t2.report_id = 2
		and t1.area_key = t2.area_key 
		and t1.month_key = t2.month_key 
	where t1.month_key = vprocess_month
	union all
	select vprocess_month, area_id, 3, 0, 0 -- Chỉ số tài chính
	from dim_area
	union all
	select vprocess_month, area_key, 27, 0, (cum_wo + npl_grp345) / (cum_wo + debt_aft_wo_month) * 100 -- tỉ lệ nợ xấu npl
	from tmp_total_dist_debt_staff_monthly t
	where month_key = vprocess_month;
	
	-- Bước 4: xóa dữ liệu xếp hạng nhân viên vào bảng fact_RK_month tại vprocess_month 
	delete from asm_rank_report where month_key = vprocess_month;

	-- Bước 4: insert dữ liệu xếp hạng nhân viên vào bảng fact_RK_month
	IF EXTRACT(YEAR FROM p_date) = 2025 AND EXTRACT(MONTH FROM p_date) = 2 then
	-- 4.1 Loan to new, psdn, approval rate
    -- 4.1.1: Tháng 2
		insert into asm_rank_report (month_key, area_cde, email, ltn_avg, psdn_avg, approval_rate_avg)
	    SELECT 
	    	vprocess_month,
	        area_code, 
	        email,
	        (jan_ltn + feb_ltn) / 2.0 AS ltn_avg, -- loan to new
	        (jan_psdn + feb_psdn) / 2.0 AS psdn_avg, -- psdn
	        (jan_appro_rate + feb_appro_rate) / 2.0 AS approval_rate_avg -- app approved
	    FROM 
        	kpi_asm k
        join 
       		dim_area d on k.area_key = d.area_id;
    ELSIF EXTRACT(MONTH FROM p_date) = 1 THEN
   	-- 4.1.2: Tháng 1
    	insert into asm_rank_report (month_key, area_cde, email, ltn_avg, psdn_avg, approval_rate_avg)
	  	SELECT 
	  		vprocess_month,
	        area_code, 
	        email,
	        jan_ltn AS ltn_avg, -- loan to new
	        jan_psdn AS psdn_avg, -- psdn
	        jan_appro_rate AS approval_rate_avg -- app approved
	    FROM 
	        kpi_asm k
        join 
       		dim_area d on k.area_key = d.area_id;
	ELSIF EXTRACT(MONTH FROM p_date) = 3 THEN
	-- 4.1.3: Tháng 3
		insert into asm_rank_report (month_key, area_cde, email, ltn_avg, psdn_avg, approval_rate_avg)
	  	SELECT 
	  		vprocess_month,
	        area_code, 
	        email,
	        (jan_ltn + feb_ltn + mar_ltn) / 3.0 AS ltn_avg, -- loan to new
	        (jan_psdn + feb_psdn + mar_psdn) / 3.0 AS psdn_avg, -- psdn
	        (jan_appro_rate + feb_appro_rate + mar_appro_rate) / 3.0 AS approval_rate_avg -- app approved
	    FROM 
	        kpi_asm k
        join 
       		dim_area d on k.area_key = d.area_id;
	ELSIF EXTRACT(MONTH FROM p_date) = 4 THEN
	    -- 4.1.4: Tháng 4
		insert into asm_rank_report (month_key, area_cde, email, ltn_avg, psdn_avg, approval_rate_avg)
	    SELECT 
	    	vprocess_month,
	        area_code, 
	        email,
	        (jan_ltn + feb_ltn + mar_ltn + apr_ltn) / 4.0 AS ltn_avg, -- loan to new
	        (jan_psdn + feb_psdn + mar_psdn + apr_psdn) / 4.0 AS psdn_avg, -- psdn
	        (jan_appro_rate + feb_appro_rate + mar_appro_rate + apr_appro_rate) / 4.0 AS approval_rate_avg -- app approved
	    FROM 
	        kpi_asm k
        join 
       		dim_area d on k.area_key = d.area_id;
	ELSIF EXTRACT(MONTH FROM p_date) = 5 THEN
	    -- 4.1.5: Tháng 5
		insert into asm_rank_report (month_key, area_cde, email, ltn_avg, psdn_avg, approval_rate_avg)
	    SELECT 
	    	vprocess_month,
	        area_code, 
	        email,
	        (jan_ltn + feb_ltn + mar_ltn + apr_ltn + may_ltn) / 5.0 AS ltn_avg, -- loan to new
	        (jan_psdn + feb_psdn + mar_psdn + apr_psdn + may_psdn) / 5.0 AS psdn_avg, -- psdn
	        (jan_appro_rate + feb_appro_rate + mar_appro_rate + apr_appro_rate + may_appro_rate) / 5.0 AS approval_rate_avg -- app approved
	    FROM 
	        kpi_asm k
        join 
       		dim_area d on k.area_key = d.area_id;
	ELSE 
	    insert into asm_rank_report 
	    values(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
	END IF;

	-- 4.2 update npl lũy kế trước wo cir, margin, hs vốn, hs bình quân nhân sự
	-- Update npl lũy kế trước wo
	update asm_rank_report r
	set npl_truoc_wo_luy_ke = (cum_wo + npl_grp345)::float / (cum_wo + debt_aft_wo_month) * 100
	from tmp_total_dist_debt_staff_monthly t
	join dim_area d on t.area_key = d.area_id 
	where r.month_key = t.month_key 
		AND r.area_cde = d.area_code 
		AND r.month_key = vprocess_month; 
	
	-- Update CIR
	UPDATE asm_rank_report r
	SET cir = amt_dist_ytm_from_gl_final  
	FROM fact_summary_report_monthly fct
	join dim_area d on fct.area_key = d.area_id 
	WHERE r.month_key = fct .month_key 
	  AND r.area_cde = d.area_code  
	  AND fct.report_id = 23
	  AND r.month_key = vprocess_month;  -- Assuming this is what you meant
	  
	-- Update Margin
	UPDATE asm_rank_report r
	SET margin = amt_dist_ytm_from_gl_final 
	FROM fact_summary_report_monthly fct 
	join dim_area d on fct.area_key = d.area_id 
	WHERE r.month_key = fct.month_key 
	  AND r.area_cde = d.area_code  
	  AND fct .report_id = 24
	  AND r.month_key = vprocess_month;
	  
	-- Update HS Von
	UPDATE asm_rank_report r
	SET hs_von = amt_dist_ytm_from_gl_final  
	FROM fact_summary_report_monthly fct
	join dim_area d on fct.area_key = d.area_id 
	WHERE r.month_key = fct.month_key 
	  AND r.area_cde = d.area_code   
	  AND fct.report_id = 25
	  AND r.month_key = vprocess_month;
	  
	-- Update HSBQ Nhan Su
	UPDATE asm_rank_report r
	SET hsbq_nhan_su = amt_dist_ytm_from_gl_final 
	FROM fact_summary_report_monthly fct
	join dim_area d on fct.area_key = d.area_id
	WHERE r.month_key = fct.month_key 
	  AND r.area_cde = d.area_code  
	  AND fct.report_id = 26  -- Changed to 26 assuming this should be different from the previous one
	  AND r.month_key = vprocess_month;

	-- 4.3 Xếp rank
	 -- 4.3.1 
	 WITH ranked AS (
	  select month_key, email, 
	         rank() OVER (ORDER BY ltn_avg desc) as rank_ltn, -- rank ltn
	         rank() OVER (ORDER BY psdn_avg desc) as rank_psdn, -- rank psdn
	         rank() OVER (ORDER BY approval_rate_avg desc) as rank_approval_rate, -- rank approval rate
	         rank() OVER (ORDER BY npl_truoc_wo_luy_ke) as rank_npl_truoc_wo_luy_ke, -- rank npl trước wo lũy kế
	         dense_rank() OVER (ORDER BY cir) as rank_cir, -- rank cir
	         dense_rank() OVER (ORDER BY margin desc) as rank_margin, -- rank margin
	         dense_rank() OVER (ORDER BY hs_von desc) as rank_hs_von, -- rank hiệu suất vốn
	         dense_rank() OVER (ORDER BY hsbq_nhan_su desc) as rank_hsbq_nhan_su -- rank hsbq nhân sự
	  FROM asm_rank_report
	  where month_key = vprocess_month 
	)
	UPDATE asm_rank_report t
	SET 
		rank_ltn = r.rank_ltn,
		rank_psdn = r.rank_psdn,
		rank_approval_rate = r.rank_approval_rate,
		rank_npl_truoc_wo_luy_ke = r.rank_npl_truoc_wo_luy_ke,
		rank_cir = r.rank_cir,
		rank_margin = r.rank_margin,
		rank_hs_von = r.rank_hs_von,
		rank_hsbq_nhan_su = r.rank_hsbq_nhan_su
	FROM ranked r
	where t.email = r.email and t.month_key = vprocess_month;

	-- 4.3.2  Quy mô, tài chính
	update asm_rank_report 
	set scale_score = rank_ltn + rank_psdn + rank_approval_rate + rank_npl_truoc_wo_luy_ke, -- điểm quy mô
		fin_score = rank_cir + rank_margin + rank_hs_von + rank_hsbq_nhan_su;  -- điểm tài chính
	
	
	with fin_scale_rank as(
		select month_key, email, rank() over(order by scale_score) rank_ptkd, rank() over(order by fin_score) rank_fin
		from asm_rank_report 
		where month_key = vprocess_month 
	) 
	update asm_rank_report t
	set 
		rank_ptkd = r.rank_ptkd, -- rank quy mô
		rank_fin = r.rank_fin -- rank tài chính 
	from fin_scale_rank r
	where t.email = r.email and t.month_key = vprocess_month;

	-- 4.4 Final
	update asm_rank_report 
	set final_score = scale_score + fin_score; -- điểm final
	
	WITH ranked AS (
	  SELECT 
	    email,
	    rank() OVER (ORDER BY final_score) AS final_rank
	  FROM asm_rank_report
	  WHERE month_key = vprocess_month
	)
	UPDATE asm_rank_report t
	SET rank_final = r.final_rank
	FROM ranked r
	WHERE t.email = r.email AND t.month_key = vprocess_month;
	
	-- 4.5 Tên khu vực
	update asm_rank_report t
	set area_name = (select area_name from dim_area d where t.area_cde = d.area_code);

	-- Bước 5:
	-- Ghi nhận khi thực hiện thành công
    INSERT INTO procedure_log(procedure_name, log_message, log_level)
    VALUES (prc_name, 'Thực hiện thành công', 'INFO');
   
   EXCEPTION
    WHEN OTHERS THEN
        -- Ghi nhận khi xảy ra lỗi
        INSERT INTO procedure_log(procedure_name, log_message, log_level)
        VALUES (prc_name, 'Lỗi: ' || SQLERRM, 'ERROR');
        RAISE;
end;
$$ language plpgsql;

call fct_summary_report_asm_ranked_monthly_prc('2025-05-2'::date)


select * 
from tmp_report_gl_by_area_monthly trgbam 
where month_key = 202502


select *
from dim_funding_structure dfs 

select *
from dim_date dd 
