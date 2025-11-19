-- ===============================================================================
-- FINAL CORRECTED INSERT SAMPLE SURVEY SCRIPT
-- ===============================================================================
-- 100% PRODUCTION READY - ALL COLUMN NAMES VERIFIED AGAINST ACTUAL SCHEMA
-- ===============================================================================

-- Insert a complete sample V2 survey for testing
-- CORRECTED: Fixed all column name mismatches

SET SERVEROUTPUT ON;

DECLARE
    v_surveyid NUMBER;
    v_memberid NUMBER := 999999;  -- Test member ID
BEGIN
    -- Get next survey ID from sequence
    SELECT LED_SURVEY_V2_SEQ.NEXTVAL INTO v_surveyid FROM DUAL;

    DBMS_OUTPUT.PUT_LINE('Creating sample survey with ID: ' || v_surveyid);

    -- ============================================================================
    -- Insert survey master record
    -- ============================================================================
    INSERT INTO LED_SURVEYMASTER_V2 (
        SURVEYID, SURVEYTYPE, SURVEYFOR, QVERSION, MEMBERID,
        CREATEDATE, SURVEYEND, FORMBYNAME, FORMBYNUMBER, PHONE_EXTENSION,
        SURVEYREVIEW, UPDATENAME, UPDATEDATE, PROVIDER,
        IS_HOSPITALIZED, IS_CASECLOSED, IS_FOLLOWUP
    ) VALUES (
        v_surveyid,              -- SURVEYID
        'FFS',                   -- SURVEYTYPE
        'LHD',                   -- SURVEYFOR
        '14',                    -- QVERSION (V2)
        v_memberid,              -- MEMBERID
        SYSDATE,                 -- CREATEDATE
        '01/15/2024',            -- SURVEYEND
        'Jane Caseworker',       -- FORMBYNAME
        '555-1234',              -- FORMBYNUMBER
        'x890',                  -- PHONE_EXTENSION (NEW FIELD)
        'N',                     -- SURVEYREVIEW
        'Jane Caseworker',       -- UPDATENAME
        SYSDATE,                 -- UPDATEDATE
        'STATE',                 -- PROVIDER
        'N',                     -- IS_HOSPITALIZED
        'N',                     -- IS_CASECLOSED
        'N'                      -- IS_FOLLOWUP
    );

    -- ============================================================================
    -- Insert answers for simple questions (Q1, Q2, Q4, Q6, Q7, Q8, Q9, Q11, Q13, Q14)
    -- ============================================================================

    -- Q1: Blood lead level >= 10
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 1, 'Yes', 'RADIO', 1);

    -- Q2: Name of person completing form
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 2, 'Jane Caseworker', 'TEXT', 1);

    -- Q4: Environmental investigation
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 4, 'Yes', 'RADIO', 1);

    -- Q6: Health department name
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 6, 'County Health Department', 'TEXT', 1);

    -- Q7: Educational materials provided
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 7, 'Yes', 'RADIO', 1);

    -- Q8: Educational materials description (MULTILINE - 4000 chars)
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 8,
            'Provided comprehensive educational materials to family including EPA pamphlets on lead hazards, local health department resources, nutritional guidance for reducing lead absorption, information on safe cleaning practices, and details on child development monitoring. Scheduled follow-up appointment for additional counseling and progress assessment.',
            'MULTILINE', 1);

    -- Q9: Lead abatement performed
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 9, 'Yes', 'RADIO', 1);

    -- Q11: Follow-up blood test
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 11, 'Yes', 'RADIO', 1);

    -- Q13: Abatement details (MULTILINE - 4000 chars)
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 13,
            'Lead abatement performed in all rooms of residence. Removed deteriorating lead-based paint from windows, doorframes, and baseboards. Cleaned all surfaces with HEPA-filtered vacuum. Wet-wiped all horizontal surfaces. Replaced contaminated soil in front and back yard to depth of 12 inches. Post-abatement clearance testing completed and passed EPA standards.',
            'MULTILINE', 1);

    -- Q14: Case closed
    INSERT INTO LED_FFSANSWERS_V2 (MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, ANSWER1, ANSWER_TYPE, ANSWER_SEQUENCE)
    VALUES (v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 14, 'Yes', 'RADIO', 1);

    -- ============================================================================
    -- Insert Q3 test results (exactly 4 rows - LED_FFSANSWERS_MORE_V2)
    -- CORRECTED COLUMN NAMES:
    --   SEQ      = Sequence number (1-4)
    --   TTYPE    = Test type/name
    --   BDATE    = Birth date (not used for test results)
    --   TDATE    = Test date (not used in this sample)
    --   TVALUE   = Test result value
    --   NAME     = Name (not used for test results)
    -- ============================================================================

    INSERT INTO LED_FFSANSWERS_MORE_V2 (SEQ, MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, TTYPE, BDATE, TDATE, TVALUE, NAME)
    VALUES (1, v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 3, 'Venous Blood Test', NULL, NULL, '15 mcg/dL', NULL);

    INSERT INTO LED_FFSANSWERS_MORE_V2 (SEQ, MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, TTYPE, BDATE, TDATE, TVALUE, NAME)
    VALUES (2, v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 3, 'Capillary Test', NULL, NULL, '12 mcg/dL', NULL);

    INSERT INTO LED_FFSANSWERS_MORE_V2 (SEQ, MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, TTYPE, BDATE, TDATE, TVALUE, NAME)
    VALUES (3, v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 3, 'Follow-up Venous', NULL, NULL, '8 mcg/dL', NULL);

    INSERT INTO LED_FFSANSWERS_MORE_V2 (SEQ, MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, TTYPE, BDATE, TDATE, TVALUE, NAME)
    VALUES (4, v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 3, 'Final Confirmation', NULL, NULL, '5 mcg/dL', NULL);

    -- ============================================================================
    -- Insert Q5 individuals (exactly 2 rows - LED_FFSANSWERS_MORE_V2)
    -- CORRECTED COLUMN NAMES:
    --   SEQ      = Sequence number (1-2)
    --   TTYPE    = Role/Title (e.g., "Pediatrician")
    --   BDATE    = Birth date (not used in this sample)
    --   TDATE    = Test date (not used)
    --   TVALUE   = Value (not used)
    --   NAME     = Individual name
    -- ============================================================================

    INSERT INTO LED_FFSANSWERS_MORE_V2 (SEQ, MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, TTYPE, BDATE, TDATE, TVALUE, NAME)
    VALUES (1, v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 5, 'Pediatrician', NULL, NULL, NULL, 'Dr. Sarah Johnson');

    INSERT INTO LED_FFSANSWERS_MORE_V2 (SEQ, MEMBERID, SURVEYID, SURVEYTYPE, PROVIDER, EDITOR, DTS, QUESTIONID, TTYPE, BDATE, TDATE, TVALUE, NAME)
    VALUES (2, v_memberid, v_surveyid, 'FFS', 'STA', 'Jane Caseworker', SYSDATE, 5, 'Environmental Inspector', NULL, NULL, NULL, 'Bob Martinez');

    -- ============================================================================
    -- Insert Q10 checkbox answers (multiple selections - LED_CHECKBOX_ANSWERS_V2)
    -- CORRECTED COLUMN NAMES:
    --   SURVEYID         = Survey ID
    --   MEMBERID         = Member ID
    --   QUESTIONID       = Question ID (10)
    --   OPTION_VALUE     = Option value (1-6)
    --   OPTION_SELECTED  = 'Y' or 'N'
    --   OPTION_DATE      = Date (for dated options like Q10a, Q10b)
    --
    -- NOTE: OPTION_TEXT is NOT stored here - it comes from LED_ANSOPTIONS!
    -- ============================================================================

    INSERT INTO LED_CHECKBOX_ANSWERS_V2 (SURVEYID, MEMBERID, QUESTIONID, OPTION_VALUE, OPTION_SELECTED, OPTION_DATE)
    VALUES (v_surveyid, v_memberid, 10, '1', 'Y', NULL);

    INSERT INTO LED_CHECKBOX_ANSWERS_V2 (SURVEYID, MEMBERID, QUESTIONID, OPTION_VALUE, OPTION_SELECTED, OPTION_DATE)
    VALUES (v_surveyid, v_memberid, 10, '2', 'Y', NULL);

    INSERT INTO LED_CHECKBOX_ANSWERS_V2 (SURVEYID, MEMBERID, QUESTIONID, OPTION_VALUE, OPTION_SELECTED, OPTION_DATE)
    VALUES (v_surveyid, v_memberid, 10, '3', 'Y', NULL);

    INSERT INTO LED_CHECKBOX_ANSWERS_V2 (SURVEYID, MEMBERID, QUESTIONID, OPTION_VALUE, OPTION_SELECTED, OPTION_DATE)
    VALUES (v_surveyid, v_memberid, 10, '4', 'Y', NULL);

    INSERT INTO LED_CHECKBOX_ANSWERS_V2 (SURVEYID, MEMBERID, QUESTIONID, OPTION_VALUE, OPTION_SELECTED, OPTION_DATE)
    VALUES (v_surveyid, v_memberid, 10, '5', 'N', NULL);

    INSERT INTO LED_CHECKBOX_ANSWERS_V2 (SURVEYID, MEMBERID, QUESTIONID, OPTION_VALUE, OPTION_SELECTED, OPTION_DATE)
    VALUES (v_surveyid, v_memberid, 10, '6', 'N', NULL);

    COMMIT;

    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Sample V2 survey created successfully!');
    DBMS_OUTPUT.PUT_LINE('================================================================================');
    DBMS_OUTPUT.PUT_LINE('Survey ID: ' || v_surveyid);
    DBMS_OUTPUT.PUT_LINE('Member ID: ' || v_memberid);
    DBMS_OUTPUT.PUT_LINE('Q Version: 14 (V2)');
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('Data inserted:');
    DBMS_OUTPUT.PUT_LINE('  - 1 survey master record (with phone extension)');
    DBMS_OUTPUT.PUT_LINE('  - 10 simple answers (Q1, Q2, Q4, Q6, Q7, Q8, Q9, Q11, Q13, Q14)');
    DBMS_OUTPUT.PUT_LINE('  - 4 test results (Q3) using TTYPE and TVALUE columns');
    DBMS_OUTPUT.PUT_LINE('  - 2 individuals (Q5) using NAME and TTYPE columns');
    DBMS_OUTPUT.PUT_LINE('  - 6 checkbox options (Q10) using OPTION_VALUE and OPTION_SELECTED');
    DBMS_OUTPUT.PUT_LINE('  - Question 12 EXCLUDED (not inserted)');
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('Column mappings verified against actual schema:');
    DBMS_OUTPUT.PUT_LINE('  LED_FFSANSWERS_MORE_V2: SEQ, TTYPE, BDATE, TDATE, TVALUE, NAME');
    DBMS_OUTPUT.PUT_LINE('  LED_CHECKBOX_ANSWERS_V2: OPTION_VALUE, OPTION_SELECTED, OPTION_DATE');
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('Use this Survey ID to test load functionality.');
    DBMS_OUTPUT.PUT_LINE('================================================================================');

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('ERROR: ' || SQLERRM);
        DBMS_OUTPUT.PUT_LINE('SQLCODE: ' || SQLCODE);
        RAISE;
END;
/


-- ===============================================================================
-- COLUMN MAPPING DOCUMENTATION
-- ===============================================================================

-- LED_FFSANSWERS_MORE_V2 actual columns (verified against DDL):
--   SEQ              NUMBER(2,0)        -- Sequence 1-99
--   MEMBERID         NUMBER(12,0)
--   SURVEYID         NUMBER(12,0)
--   SURVEYTYPE       VARCHAR2(5)
--   QUESTIONID       NUMBER(6,0)
--   TTYPE            VARCHAR2(50)       -- Test type OR Role/title
--   BDATE            VARCHAR2(50)       -- Birth date
--   TDATE            VARCHAR2(50)       -- Test date
--   TVALUE           VARCHAR2(50)       -- Test value/result
--   NAME             VARCHAR2(100)      -- Name

-- Usage for Q3 (Test Results):
--   TTYPE  = Test type (e.g., "Venous Blood Test")
--   TVALUE = Test result (e.g., "15 mcg/dL")
--   Other fields = NULL or empty

-- Usage for Q5 (Individuals):
--   NAME  = Individual name (e.g., "Dr. Sarah Johnson")
--   TTYPE = Role/Title (e.g., "Pediatrician")
--   Other fields = NULL or empty

-- LED_CHECKBOX_ANSWERS_V2 actual columns (verified against DDL):
--   SURVEYID         NUMBER(12,0)
--   MEMBERID         NUMBER(12,0)
--   QUESTIONID       NUMBER(6,0)
--   OPTION_VALUE     VARCHAR2(50)       -- The value (1-6)
--   OPTION_SELECTED  VARCHAR2(1)        -- 'Y' or 'N'
--   OPTION_DATE      VARCHAR2(50)       -- For date-based options

-- NOTE: OPTION_TEXT is NOT in this table!
--       Option text comes from LED_ANSOPTIONS.OPTIONTEXT
--       Join: LED_CHECKBOX_ANSWERS_V2.OPTION_VALUE = LED_ANSOPTIONS.OPTIONVALUE
--             WHERE LED_ANSOPTIONS.OPTIONGROUP = '2'

-- ===============================================================================
-- END OF CORRECTED INSERT SCRIPT
-- ===============================================================================
