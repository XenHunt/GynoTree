CREATE OR REPLACE FUNCTION count_family_members(family_id INT) 
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(*)
        FROM Families_Persons fp
        WHERE fp.id_family = family_id
    );
END;
$$ LANGUAGE plpgsql;
