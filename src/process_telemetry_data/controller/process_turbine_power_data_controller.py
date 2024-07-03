from flask import Blueprint, request, jsonify
from src.process_telemetry_data.business_logic.service.process_turbine_telemetry_power_data_service import TimesequenceService
from flask_restful import Resource


timesequence_bp = Blueprint("timesequence", __name__)
timesequence_service = TimesequenceService()

class ProcessTimesequence(Resource):
    def post(self):
        """
        Process Telemetry Data endpoint.

        ---
        tags:
        - Telemetry
        parameters:
        - name: data
          in: body
          description: JSON data containing telemetry information
          required: true
          schema:
            type: object
            properties:
              turbine:
                type: string
                description: Name of the turbine
              power_unit:
                type: string
                description: Unit of power measurement
              timeseries:
                type: array
                description: List of timestamp-value pairs
                items:
                  type: object
                  properties:
                    timestamp:
                      type: integer
                      format: int64
                      description: Timestamp in milliseconds
                    value:
                      type: number
                      description: Value of telemetry data
                      nullable: true
        responses:
          200:
            description: Success response
            schema:
              type: object
              properties:
                modified_data:
                  type: string
                  description: Description of modified data
          400:
            description: Bad request
        """
        data = request.json
        modified_data = timesequence_service.process_data(data)
        print(modified_data)
        return modified_data, 200


