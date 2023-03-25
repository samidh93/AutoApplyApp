@echo off

set access_token= AQVe5mMR9PrYXSSHibldnBQpwe6jen_ci-iVPN-76DcXIFchqQwS2PdCygAmcOjp-aTgJc-gIyHaiqzUjoHziM9NMqT8RpiVImBYxWrAEQazh7ZsdkmeQWWz0_Jt9fudyg3-7YT7h9S8DPyVS_l1C1C0VGhSvrw7FxHb2smsSs0WdfONhb5EjRvUXt2ozaWPWoQiNd2piORAoYeP5ebTqLpp-XqGvgSzctShBZwlyM0ico2dTGhT4lHL-NyTsQU67HdMg3jJECaRDvnnVfubju0V73cjT7hZif4x5uRv8YZzx7lttFzvyZvYUfDlTzIbWpMBdBjjoQgCWJGDZ3sY1OkBr0l0gQ

curl --location --request GET "https://api.linkedin.com/v2/job-search" ^
--header "Authorization: Bearer %access_token%" ^
--header "Content-Type: application/json" ^
--data-raw "{
    \"job-title\": \"software engineer\",
    \"locations\": [
        {
            \"country\": \"us\",
            \"postal-code\": \"94043\"
        }
    ]
}"
