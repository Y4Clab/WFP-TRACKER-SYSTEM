from drf_yasg import openapi

# Vendor schemas
vendor_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['name', 'city', 'country'],
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Vendor company name'),
        'city': openapi.Schema(type=openapi.TYPE_STRING, description='Vendor city'),
        'country': openapi.Schema(type=openapi.TYPE_STRING, description='Vendor country'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Vendor email'),
        'website': openapi.Schema(type=openapi.TYPE_STRING, description='Vendor website'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Vendor address'),
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Vendor phone'),
    }
)

vendor_response = openapi.Response(
    description="Vendor created successfully",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'unique_id': openapi.Schema(type=openapi.TYPE_STRING, example="123e4567-e89b-12d3-a456-426614174000"),
            'name': openapi.Schema(type=openapi.TYPE_STRING, example="Acme Logistics"),
            'city': openapi.Schema(type=openapi.TYPE_STRING, example="New York"),
            'country': openapi.Schema(type=openapi.TYPE_STRING, example="USA"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, example="contact@acmelogistics.com"),
            'website': openapi.Schema(type=openapi.TYPE_STRING, example="https://acmelogistics.com"),
            'address': openapi.Schema(type=openapi.TYPE_STRING, example="123 Main St, New York, NY"),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, example="+1-555-123-4567"),
            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example="2023-07-21T17:32:28Z"),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        }
    )
)

# Truck schemas
truck_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['plate_number', 'vendor', 'capacity_tons'],
    properties={
        'plate_number': openapi.Schema(type=openapi.TYPE_STRING, description='Truck plate number'),
        'vendor': openapi.Schema(type=openapi.TYPE_STRING, description='Vendor unique ID'),
        'capacity_tons': openapi.Schema(type=openapi.TYPE_NUMBER, description='Truck capacity in tons'),
        'model': openapi.Schema(type=openapi.TYPE_STRING, description='Truck model'),
        'year': openapi.Schema(type=openapi.TYPE_INTEGER, description='Truck manufacturing year'),
        'registration_document': openapi.Schema(type=openapi.TYPE_STRING, description='Registration document URL'),
        'insurance_document': openapi.Schema(type=openapi.TYPE_STRING, description='Insurance document URL'),
    }
)

truck_response = openapi.Response(
    description="Truck created successfully",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'unique_id': openapi.Schema(type=openapi.TYPE_STRING, example="123e4567-e89b-12d3-a456-426614174001"),
            'plate_number': openapi.Schema(type=openapi.TYPE_STRING, example="ABC123"),
            'vendor': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'unique_id': openapi.Schema(type=openapi.TYPE_STRING, example="123e4567-e89b-12d3-a456-426614174000"),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, example="Acme Logistics"),
                }
            ),
            'capacity_tons': openapi.Schema(type=openapi.TYPE_NUMBER, example=10.5),
            'model': openapi.Schema(type=openapi.TYPE_STRING, example="Volvo FH16"),
            'year': openapi.Schema(type=openapi.TYPE_INTEGER, example=2020),
            'registration_document': openapi.Schema(type=openapi.TYPE_STRING, example="http://example.com/docs/reg123.pdf"),
            'insurance_document': openapi.Schema(type=openapi.TYPE_STRING, example="http://example.com/docs/ins123.pdf"),
            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example="2023-07-21T17:32:28Z"),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        }
    )
)

# Truck-Mission Assignment schemas
truck_mission_assignment_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['truck', 'mission', 'driver'],
    properties={
        'truck': openapi.Schema(type=openapi.TYPE_STRING, description='Truck unique ID'),
        'mission': openapi.Schema(type=openapi.TYPE_STRING, description='Mission unique ID'),
        'driver': openapi.Schema(type=openapi.TYPE_STRING, description='Driver unique ID'),
        'cargo_items_ids': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING),
            description='List of cargo item unique IDs'
        ),
        'planned_departure_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Planned departure date'),
        'actual_departure_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Actual departure date', nullable=True),
        'planned_arrival_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Planned arrival date'),
        'actual_arrival_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Actual arrival date', nullable=True),
        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Assignment status'),
    }
)

# Cargo item assignment to truck schemas
cargo_assignment_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['cargo_items'],
    properties={
        'cargo_items': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'cargo_item_id': openapi.Schema(type=openapi.TYPE_STRING, description='Cargo item unique ID'),
                    'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of cargo item'),
                }
            ),
            description='List of cargo items with quantities'
        )
    }
) 