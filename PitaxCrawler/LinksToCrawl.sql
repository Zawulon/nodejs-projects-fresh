UPDATE [LinksToCrawl]
	SET 
		[UrlToCrawl] = 'http://' || [UrlToCrawl]
		
	WHERE 
	 [UseForCrawl] = 'yes'
and UrlToCrawl not like 'http%'



SELECT 
--'http://' || 
[UrlToCrawl]
FROM [LinksToCrawl]
where [UseForCrawl] = 'yes'
and UrlToCrawl not like 'http%'

delete FROM [LinksToCrawl]
where UrlToCrawl = 'UrlToCrawl'



update LinksToCrawl
set UseForCrawl = 'no'
where UrlToCrawl IN
(
SELECT [UrlToCrawl]
FROM [LinksToCrawl]
group by UrlToCrawl
having count(1) > 1
)


SELECT 
--'http://' || 
[UrlToCrawl], rank
FROM [LinksToCrawl]
where [UseForCrawl] = 'no'
order by UrlToCrawl


with un as
(
SELECT
   MIN(A.LinkId) as minling,
   MAX(B.LinkId) as maxling,
   --A.LinkId As LinkId,
   --B.LinkId As LinkIdID,
   A.UrlToCrawl
FROM
   -- Every pair of master records:
   LinksToCrawl As A
   JOIN
   LinksToCrawl As B
   ON (A.UrlToCrawl = B.UrlToCrawl)
WHERE
   -- Only those pairs where A is earlier than B:
   A.LinkId < B.LinkId
  group by A.UrlToCrawl
  
  )
 update LinksToCrawl
 set [UseForCrawl] = 'no'
 --select t1.UseForCrawl
 from LinksToCrawl 
  INNER JOIN un
  ON UrlToCrawl = un.UrlToCrawl
  and LinkId < un.maxling
  



SELECT min([LinkId]) as LinkId
	,[UrlToCrawl]
	
FROM [LinksToCrawl]
--where [UseForCrawl] = 'yes'
group by UrlToCrawl
ORDER BY [LinkId] DESC LIMIT 500