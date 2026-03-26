def get_area_bucket(area_sqft):
    if area_sqft < 1000:
        return "small"

    bucket_start = (area_sqft // 500) * 500
    bucket_end = bucket_start + 500

    return f"{int(bucket_start)}-{int(bucket_end)}"