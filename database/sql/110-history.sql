SET QUOTED_IDENTIFIER ON;
GO

IF (SCHEMA_ID('chainlit') IS NULL) BEGIN
    EXEC('CREATE SCHEMA [chainlit] AUTHORIZATION dbo;')
END
GO

-- DROP TABLE IF EXISTS [chainlit].[threads];
-- DROP TABLE IF EXISTS [chainlit].[users];
-- DROP TABLE IF EXISTS [chainlit].[steps];
-- DROP TABLE IF EXISTS [chainlit].[elements];
-- DROP TABLE IF EXISTS [chainlit].[feedbacks];
-- GO

IF OBJECT_ID('[chainlit].[users]') IS NULL 
    CREATE TABLE [chainlit].[users] 
    (
        "id" UNIQUEIDENTIFIER PRIMARY KEY,
        "identifier" VARCHAR(1000) COLLATE Latin1_General_100_BIN2 NOT NULL UNIQUE,
        "metadata" JSON NOT NULL,
        "createdAt" NVARCHAR(MAX)
    );

IF OBJECT_ID('[chainlit].[threads]') IS NULL 
    CREATE TABLE [chainlit].[threads] (
        "id" UNIQUEIDENTIFIER PRIMARY KEY,
        "createdAt" DATETIME2(7),
        "name" NVARCHAR(1000),
        "userId" UNIQUEIDENTIFIER,
        "userIdentifier" VARCHAR(1000) COLLATE Latin1_General_100_BIN2,
        "tags" NVARCHAR(MAX),
        "metadata" JSON,
        FOREIGN KEY ("userId") REFERENCES [chainlit].[users] ("id") ON DELETE CASCADE
    );

IF OBJECT_ID('[chainlit].[steps]') IS NULL 
    CREATE TABLE [chainlit].[steps] (
        "id" UNIQUEIDENTIFIER PRIMARY KEY,
        "name" NVARCHAR(1000) NOT NULL,
        "type" NVARCHAR(1000) NOT NULL,
        "threadId" UNIQUEIDENTIFIER NOT NULL,
        "parentId" UNIQUEIDENTIFIER,
        "disableFeedback" BIT NOT NULL,
        "streaming" BIT NOT NULL,
        "waitForAnswer" BIT,
        "isError" BIT,
        "metadata" JSON,
        "tags" NVARCHAR(MAX),
        "input" NVARCHAR(MAX),
        "output" NVARCHAR(MAX),
        "createdAt" DATETIME2(7),
        "start" NVARCHAR(MAX),
        "end" NVARCHAR(MAX),
        "generation" JSON,
        "showInput" NVARCHAR(MAX),
        "language" NVARCHAR(MAX),
        "indent" INT
    );

IF OBJECT_ID('[chainlit].[elements]') IS NULL 
    CREATE TABLE [chainlit].[elements] (
        "id" UNIQUEIDENTIFIER PRIMARY KEY,
        "threadId" UNIQUEIDENTIFIER,
        "type" NVARCHAR(MAX),
        "url" NVARCHAR(MAX),
        "chainlitKey" NVARCHAR(MAX),
        "name" NVARCHAR(MAX) NOT NULL,
        "display" NVARCHAR(MAX),
        "objectKey" NVARCHAR(MAX),
        "size" NVARCHAR(MAX),
        "page" INT,
        "language" NVARCHAR(MAX),
        "forId" UNIQUEIDENTIFIER,
        "mime" NVARCHAR(MAX)
    );

IF OBJECT_ID('[chainlit].[feedbacks]') IS NULL 
    CREATE TABLE [chainlit].[feedbacks] (
        "id" UNIQUEIDENTIFIER PRIMARY KEY,
        "forId" UNIQUEIDENTIFIER NOT NULL,
        "threadId" UNIQUEIDENTIFIER NOT NULL,
        "value" INT NOT NULL,
        "comment" NVARCHAR(MAX)
    );

