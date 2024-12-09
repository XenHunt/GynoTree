INSERT INTO families (id, name) VALUES
(DEFAULT, 'Барановы');

-- INSERT INTO families VALUES ('Ивановы'), ('Петровы'), ('Сидоровы');


INSERT INTO persons (id, firstname, lastName, middleName, is_male) VALUES
(DEFAULT, 'Иван', 'Баранов', 'Иванович', TRUE),
(DEFAULT, 'Мария', 'Баранова', 'Ивановна', FALSE),
(DEFAULT, 'Пётр', 'Петров', 'Петрович', TRUE),
(DEFAULT, 'Анна', 'Петрова', 'Петровна', FALSE),
(DEFAULT, 'Сидор', 'Петровы', 'Сидорович', TRUE),
(DEFAULT, 'Елена', 'Петрова', 'Сидоровна', FALSE);

INSERT INTO families_persons (id_family, id_person) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6);

-- SELECT * FROM parentschildrenrelationships;

INSERT INTO parents_children_relationships (parent_id, child_id) VALUES
(1, 2),  
(1, 3),  
(2, 4),
(2, 5),
(2, 6),
(3, 4),
(3, 5),
(3,6);  
