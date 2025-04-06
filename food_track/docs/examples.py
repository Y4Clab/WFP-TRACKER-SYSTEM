# Vendor examples
vendor_request_example = {
    "name": "Acme Logistics",
    "city": "New York",
    "country": "USA",
    "email": "contact@acmelogistics.com",
    "website": "https://acmelogistics.com",
    "address": "123 Main St, New York, NY",
    "phone": "+1-555-123-4567"
}

vendor_response_example = {
    "unique_id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Acme Logistics",
    "city": "New York",
    "country": "USA",
    "email": "contact@acmelogistics.com",
    "website": "https://acmelogistics.com",
    "address": "123 Main St, New York, NY",
    "phone": "+1-555-123-4567",
    "created_at": "2023-07-21T17:32:28Z",
    "is_active": True
}

# Truck examples
truck_request_example = {
    "plate_number": "ABC123",
    "vendor": "123e4567-e89b-12d3-a456-426614174000",
    "capacity_tons": 10.5,
    "model": "Volvo FH16",
    "year": 2020,
    "registration_document": "http://example.com/docs/reg123.pdf",
    "insurance_document": "http://example.com/docs/ins123.pdf"
}

truck_response_example = {
    "unique_id": "123e4567-e89b-12d3-a456-426614174001",
    "plate_number": "ABC123",
    "vendor": {
        "unique_id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Acme Logistics"
    },
    "capacity_tons": 10.5,
    "model": "Volvo FH16",
    "year": 2020,
    "registration_document": "http://example.com/docs/reg123.pdf",
    "insurance_document": "http://example.com/docs/ins123.pdf",
    "created_at": "2023-07-21T17:32:28Z",
    "is_active": True
}

# Truck-Mission Assignment examples
truck_mission_assignment_example = {
    "truck": "123e4567-e89b-12d3-a456-426614174001",
    "mission": "423e4567-e89b-12d3-a456-426614174333",
    "driver": "523e4567-e89b-12d3-a456-426614174444",
    "cargo_items_ids": [
        "623e4567-e89b-12d3-a456-426614174555",
        "723e4567-e89b-12d3-a456-426614174666"
    ],
    "planned_departure_date": "2023-08-01",
    "actual_departure_date": None,
    "planned_arrival_date": "2023-08-05",
    "actual_arrival_date": None,
    "status": "Pending"
}

# Cargo Assignment examples
cargo_assignment_example = {
    "cargo_items": [
        {
            "cargo_item_id": "623e4567-e89b-12d3-a456-426614174555",
            "quantity": 50
        },
        {
            "cargo_item_id": "723e4567-e89b-12d3-a456-426614174666",
            "quantity": 25
        }
    ]
} 