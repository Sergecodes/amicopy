
- setup django-admin, with grappelli too
- setup s3 bucket
- write test for forms, models, views
- test docker


# source /home/sergeman/.virtualenvs/amicopy-env/bin/activate



4. Trigger on transactions.device to ensure both browser_session_id and user_id can't be null.
CREATE OR REPLACE FUNCTION check_device_owner() RETURNS trigger AS $check_device_owner$
    BEGIN 
        IF NEW.browser_session_id = '' AND NEW.user_id IS NULL THEN
            RAISE EXCEPTION 'Both browser_session_id and user_id can''t be unset';
        END IF;
        RETURN NEW;
    END;
    $check_device_owner$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_device_owner BEFORE INSERT OR UPDATE ON transactions.device
    FOR EACH ROW EXECUTE FUNCTION check_device_owner();
