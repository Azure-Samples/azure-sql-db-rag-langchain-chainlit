insert into web.speakers
    (id, full_name, require_embeddings_update)
values
    (5000, 'John Doe', 0)
go

declare @t as nvarchar(max), @e as varbinary(8000)
select @t = full_name from web.speakers where id = 5000
exec web.get_embedding @t, @e output
update web.speakers set embeddings = @e where id = 5000
go

insert into web.sessions 
    (id, title, abstract, external_id, start_time, end_time, require_embeddings_update)
values
    (
        1000,
        'Building a session recommender using OpenAI and Azure SQL', 
        'In this fun and demo-driven session you''ll learn how to integrate Azure SQL with OpenAI to generate text embeddings, store them in the database, index them and calculate cosine distance to build a session recommender. And once that is done, you''ll publish it as a REST and GraphQL API to be consumed by a modern JavaScript frontend. Sounds pretty cool, uh? Well, it is!',
        'S1',
        '2024-06-01 10:00:00',
        '2024-06-01 11:00:00',
        0
    )
go

declare @t as nvarchar(max), @e as varbinary(8000)
select @t = title + ':' + abstract from web.sessions where id = 1000
exec web.get_embedding @t, @e output
update web.sessions set embeddings = @e where id = 1000
go

insert into web.sessions_speakers
    (session_id, speaker_id)
values
    (1000, 5000)
go

insert into web.sessions 
    (id, title, abstract, external_id, start_time, end_time, require_embeddings_update)
values
    (
        1001,
        'Unlock the Art of Pizza Making with John Doe!', 
        'Whether you''re an avid home pizza oven enthusiast, contemplating a purchase, or nurturing dreams of launching your very own pizza venture, this course is tailor-made for you! Join John Doe, the visionary behind Great Pizza, as he guides you through the captivating world of pizza craftsmanship. With over six years of experience running his thriving pizza business, John has honed his skills to perfection, earning the title of a master pizzaiolo. Before embarking on his entrepreneurial journey, John—a former chef—also completed a pizza-making course at The School. Now, he''s excited to share his expertise with you in this hands-on workshop. During the course, you''ll learn to create three distinct pizza styles: Neapolitan, thin Roman “Tonda,” and Calzone. Dive into the art of dough preparation, experimenting with both high and low hydration doughs, all while adjusting temperatures to achieve pizza perfection. Don''t miss this opportunity to elevate your pizza-making game and impress your taste buds! ',
        'S2',
        '2024-06-01 11:00:00',
        '2024-06-01 12:00:00',
        0
    )
go

declare @t as nvarchar(max), @e as varbinary(8000)
select @t = title + ':' + abstract from web.sessions where id = 1001
exec web.get_embedding @t, @e output
update web.sessions set embeddings = @e where id = 1001
go

insert into web.sessions_speakers
    (session_id, speaker_id)
values
    (1001, 5000)
go


insert into web.sessions 
    (id, title, abstract, external_id, start_time, end_time, require_embeddings_update)
values
    (
        1002,
        'RAG on Azure SQL', 
        'RAG (Retrieval Augmented Generation) is the most common approach used to get LLMs to answer questions grounded in a particular domain''s data. How do you build a RAG solution on data already stored in SQL Server or Azure SQL? In this session you''ll learn about existing and future options that you can start to use right tomorrow, leveraging Azure SQL as a vector store and taking advantage of its established performances, security and enterprise readiness!',
        'R1',
        '2024-09-05 16:00:00',
        '2024-09-05 17:00:00',
        0
    )
go

declare @t as nvarchar(max), @e as varbinary(8000)
select @t = title + ':' + abstract from web.sessions where id = 1001
exec web.get_embedding @t, @e output
update web.sessions set embeddings = @e where id = 1001
go

insert into web.sessions_speakers
    (session_id, speaker_id)
values
    (1002, 5000)
go