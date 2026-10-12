-- This function allows the React app to refresh the materialized view
-- after new data is uploaded via AdminUpload.jsx.

CREATE OR REPLACE FUNCTION refresh_material_metrics()
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER -- Ensures the function runs with admin privileges
AS $$
BEGIN
    -- Refresh the materialized view so it pulls the latest data from product_metrics
    REFRESH MATERIALIZED VIEW category_material_metrics;
END;
$$;
