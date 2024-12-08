CREATE OR REPLACE FUNCTION count_male_family_members(family_id INT) 
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(*)
        FROM Families_Persons fp
        JOIN Persons p ON fp.id_person = p.id
        WHERE fp.id_family = family_id AND p.is_male = TRUE
    );
END;
$$ LANGUAGE plpgsql;
