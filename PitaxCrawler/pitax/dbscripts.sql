CREATE TABLE [PitaxCrawlResult] (
	[crawl_date] datetime NOT NULL, 
	[crawl_url] nvarchar(512) NOT NULL, 
	[crawl_status] int NOT NULL, 
	[crawl_found] int NOT NULL, 
	[link_text] nvarchar(512),
	[headers] nvarchar(2048),
	[parse_time] nvarchar(128) NOT NULL,	
	[crawl_title] nvarchar(512) NOT NULL
);

CREATE TABLE [LinkRole] (
	[Role] char(8) NOT NULL PRIMARY KEY, 
	[Description] nvarchar(2048) NOT NULL, 
	[RegexMatch] nvarchar(254)
);

CREATE TABLE [LinksToCrawl] (
	[LinkId] integer NOT NULL PRIMARY KEY, 
	[UrlToCrawl] nvarchar(2048) NOT NULL, 
	[Account] nvarchar(2048) NOT NULL, 
	[UseForCrawl] yesno NOT NULL DEFAULT yes, 
	[Created_date] datetime NOT NULL DEFAULT (DATETIME('NOW','UTC')), 
	[Modify_date] datetime NOT NULL DEFAULT (DATETIME('NOW','UTC'))
);

CREATE TABLE [Ogranization] (
	[Account] char(8) NOT NULL PRIMARY KEY, 
	[Name] nvarchar(2048) NOT NULL, 
	[Phone] nvarchar(254), 
	[Email] nvarchar(254), 
	[Contact] nvarchar(254)
);

CREATE TABLE [ScheduleCrawl] (
	[CrawlDate] datetime NOT NULL DEFAULT (DATETIME('NOW','UTC')), 
	[LinkId] char(26) NOT NULL, 
	FOREIGN KEY ([LinkId])
		REFERENCES [LinksToCrawl] ([LinkId])
		ON UPDATE NO ACTION ON DELETE CASCADE
);


CREATE VIEW [report_7_days] AS
select	report_date,
	  crawl_url,
	 count(1) rows,
	 sum(crawl_found) as suma
from
(	
select 
(
select date(max(crawl_date),
	 '-7 day') from PitaxCrawlResult) as report_date
,
	date([crawl_date]) as crawl_date
,
	crawl_url
,
	max([crawl_found]) as crawl_found
from PitaxCrawlResult
where date(crawl_date) >= report_date
group by date([crawl_date]),
	 crawl_url
order by crawl_url,
	 date(crawl_date) desc
)
group by report_date,
	 crawl_url
having suma < rows
and suma > 0;


CREATE VIEW [report_3_days] AS
select	report_date,
	  crawl_url,
	 count(1) rows,
	 sum(crawl_found) as suma
from
(	
select 
(
select date(max(crawl_date),
	 '-3 day') from PitaxCrawlResult) as report_date
,
	date([crawl_date]) as crawl_date
,
	crawl_url
,
	max([crawl_found]) as crawl_found
from PitaxCrawlResult
where date(crawl_date) >= report_date
group by date([crawl_date]),
	 crawl_url
order by crawl_url,
	 date(crawl_date) desc
)
group by report_date,
	 crawl_url
having suma < rows
and suma > 0;

CREATE VIEW [report_todays] AS
select	report_date,
				  crawl_url,
				 count(1) rows,
				 sum(crawl_found) as suma
from
(	
select 
(
select date(max(crawl_date)) from PitaxCrawlResult) as report_date
,
				date([crawl_date]) as crawl_date
,
				crawl_url
,
				max([crawl_found]) as crawl_found
from PitaxCrawlResult
where date(crawl_date) >= report_date
group by date([crawl_date]),
				 crawl_url
order by crawl_url,
				 date(crawl_date) desc
)
group by report_date,
				 crawl_url
having suma < rows;