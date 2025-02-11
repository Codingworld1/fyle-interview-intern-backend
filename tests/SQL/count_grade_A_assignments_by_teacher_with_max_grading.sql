-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherGradingCounts AS (
    SELECT
        teacher_id,
        COUNT(*) AS total_graded
    FROM
        assignments
    WHERE
        grade IS NOT NULL
    GROUP BY
        teacher_id
),
TopTeacher AS (
    SELECT
        teacher_id
    FROM
        TeacherGradingCounts
    ORDER BY
        total_graded DESC
    LIMIT 1
)
SELECT
    COUNT(*) AS grade_A_count
FROM
    assignments
WHERE
    grade = 'A'
    AND teacher_id = (SELECT teacher_id FROM TopTeacher);








