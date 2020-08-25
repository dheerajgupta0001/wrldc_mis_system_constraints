CREATE TABLE TRANSMISSION_CONSTRAINT_DATA (
    ID NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY,
    start_date DATE NOT NULL,
    end_DATE DATE NOT NULL,
    corridor VARCHAR2(1000 BYTE) not null,
    season_antecedent VARCHAR2(1000 BYTE),
    description_constraints VARCHAR2(1000 BYTE),
    primary key(id)
)