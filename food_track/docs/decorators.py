from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import examples
from food_track.serializers import (
    VendorCreateSerializer, VendorGetSerializer,
    TruckCreateSerializer, TruckGetSerializer,
    TrucksForMissionCreateSerializer, TrucksForMissionGetSerializer,
    ContactGetSerializer, MissionGetSerializer
)

def vendor_create_docs(view_func):
    """Decorator to document vendor creation endpoint"""
    return swagger_auto_schema(
        request_body=VendorCreateSerializer,
        responses={
            201: VendorGetSerializer,
            400: "Invalid vendor data"
        },
        operation_description="Create a new vendor",
        examples={
            'application/json': examples.vendor_request_example
        }
    )(view_func)

def truck_create_docs(view_func):
    """Decorator to document truck creation endpoint"""
    return swagger_auto_schema(
        request_body=TruckCreateSerializer,
        responses={
            201: TruckGetSerializer,
            400: "Invalid truck data"
        },
        operation_description="Create a new truck",
        examples={
            'application/json': examples.truck_request_example
        }
    )(view_func)

def truck_mission_assignment_docs(view_func):
    """Decorator to document truck-mission assignment endpoint"""
    return swagger_auto_schema(
        request_body=TrucksForMissionCreateSerializer,
        responses={
            201: TrucksForMissionGetSerializer,
            400: "Invalid assignment data"
        },
        operation_description="Assign a truck to a mission with cargo items",
        examples={
            'application/json': examples.truck_mission_assignment_example
        }
    )(view_func)

def cargo_assignment_docs(view_func):
    """Decorator to document cargo assignment endpoint"""
    return swagger_auto_schema(
        request_body=openapi.Schema(
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
        ),
        responses={
            200: "Cargo items assigned to truck successfully",
            400: "Invalid cargo assignment data",
            404: "Truck assignment not found"
        },
        operation_description="Assign cargo items to a truck for a mission",
        examples={
            'application/json': examples.cargo_assignment_example
        }
    )(view_func)

def vendor_data_docs(view_func):
    """Decorator to document vendor data retrieval endpoint"""
    return swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Vendor data retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'vendor': VendorGetSerializer,
                        'contacts': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=ContactGetSerializer
                        ),
                        'trucks': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=TruckGetSerializer
                        ),
                        'missions': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=MissionGetSerializer
                        ),
                    }
                )
            ),
            404: "No vendor association found for this user"
        },
        operation_description="Get all data related to the vendor associated with the authenticated user"
    )(view_func) 