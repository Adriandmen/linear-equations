CREATE TABLE users (
    ID              INT             NOT NULL AUTO_INCREMENT,
    Username        VARCHAR(255),
    Rating          DOUBLE          NOT NULL,
    KFactor         DOUBLE          NOT NULL,
    RandomID        VARCHAR(32)     NOT NULL,
    UNIQUE (ID),
    UNIQUE (RandomID),
    
    PRIMARY KEY (ID)
);

CREATE TABLE equations (
    ID               INT             NOT NULL AUTO_INCREMENT,
    LeftEquation     VARCHAR(255)    NOT NULL,
    RightEquation    VARCHAR(255)    NOT NULL,
    Variable         VARCHAR(32)     NOT NULL,
    Rating           INT             NOT NULL,
    UNIQUE (ID),
    
    PRIMARY KEY (ID)
);

CREATE TABLE progress (
    ID             INT             NOT NULL AUTO_INCREMENT,
    UserID         INT             NOT NULL,
    EquationID     INT             NOT NULL,
    Correct        BOOL,
    RatingGain     DOUBLE,
    UserAnswer     VARCHAR(255),
    StartDate      DATE            NOT NULL,
    UNIQUE (ID),
    
    PRIMARY KEY (ID),
    FOREIGN KEY (UserID) REFERENCES Users(ID),
    FOREIGN KEY (EquationID) REFERENCES Equations(ID)
);