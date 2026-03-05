"""Task 2: Simple Reflex Agent for Air Quality Index (AQI) Calculation

This module implements a simple reflex agent that takes environmental parameters
from sensors and calculates the Air Quality Index (AQI) for the region.

The agent uses condition-action rules to determine the AQI based on pollutant levels.
"""

import math


class AQIReflexAgent:
    """A simple reflex agent for calculating AQI based on sensor inputs."""
    
    def __init__(self):
        """Initialize the reflex agent with AQI breakpoints and pollutant information."""
        # AQI breakpoints for PM2.5 (in µg/m³)
        self.pm25_breakpoints = [
            (0.0, 12.0, 0, 50),      # Good
            (12.1, 35.4, 51, 100),   # Moderate
            (35.5, 55.4, 101, 150),  # Unhealthy for Sensitive Groups
            (55.5, 150.4, 151, 200), # Unhealthy
            (150.5, 250.4, 201, 300),# Very Unhealthy
            (250.5, 500.0, 301, 500) # Hazardous
        ]
        
        # AQI breakpoints for PM10 (in µg/m³)
        self.pm10_breakpoints = [
            (0, 54, 0, 50),
            (55, 154, 51, 100),
            (155, 254, 101, 150),
            (255, 354, 151, 200),
            (355, 424, 201, 300),
            (425, 604, 301, 500)
        ]
        
        # AQI breakpoints for O3 (8-hour, in ppm)
        self.o3_breakpoints = [
            (0.000, 0.054, 0, 50),
            (0.055, 0.070, 51, 100),
            (0.071, 0.085, 101, 150),
            (0.086, 0.105, 151, 200),
            (0.106, 0.200, 201, 300)
        ]
        
        # AQI breakpoints for CO (8-hour, in ppm)
        self.co_breakpoints = [
            (0.0, 4.4, 0, 50),
            (4.5, 9.4, 51, 100),
            (9.5, 12.4, 101, 150),
            (12.5, 15.4, 151, 200),
            (15.5, 30.4, 201, 300),
            (30.5, 50.4, 301, 500)
        ]
        
        # AQI breakpoints for NO2 (1-hour, in ppb)
        self.no2_breakpoints = [
            (0, 53, 0, 50),
            (54, 100, 51, 100),
            (101, 360, 101, 150),
            (361, 649, 151, 200),
            (650, 1249, 201, 300),
            (1250, 2049, 301, 500)
        ]
        
        # AQI categories
        self.aqi_categories = {
            (0, 50): "Good",
            (51, 100): "Moderate",
            (101, 150): "Unhealthy for Sensitive Groups",
            (151, 200): "Unhealthy",
            (201, 300): "Very Unhealthy",
            (301, 500): "Hazardous"
        }
    
    def calculate_individual_aqi(self, concentration, breakpoints):
        """Calculate AQI for a specific pollutant using the EPA formula.
        
        Args:
            concentration: Current concentration of the pollutant
            breakpoints: List of (C_low, C_high, I_low, I_high) tuples
            
        Returns:
            Calculated AQI value for the pollutant
        """
        for c_low, c_high, i_low, i_high in breakpoints:
            if c_low <= concentration <= c_high:
                # EPA AQI formula: I = ((I_high - I_low) / (C_high - C_low)) * (C - C_low) + I_low
                aqi = ((i_high - i_low) / (c_high - c_low)) * (concentration - c_low) + i_low
                return round(aqi)
        
        # If concentration exceeds all breakpoints, return hazardous level
        return 500
    
    def get_aqi_category(self, aqi):
        """Get the AQI category based on the AQI value.
        
        Args:
            aqi: The calculated AQI value
            
        Returns:
            String describing the AQI category
        """
        for (low, high), category in self.aqi_categories.items():
            if low <= aqi <= high:
                return category
        return "Beyond AQI"
    
    def get_health_recommendations(self, aqi):
        """Provide health recommendations based on AQI level.
        
        Args:
            aqi: The calculated AQI value
            
        Returns:
            String with health recommendations
        """
        if aqi <= 50:
            return "Air quality is satisfactory. Air pollution poses little or no risk."
        elif aqi <= 100:
            return "Air quality is acceptable. Unusually sensitive people should consider limiting prolonged outdoor exertion."
        elif aqi <= 150:
            return "Members of sensitive groups may experience health effects. The general public is less likely to be affected."
        elif aqi <= 200:
            return "Everyone may begin to experience health effects. Members of sensitive groups may experience more serious effects."
        elif aqi <= 300:
            return "Health alert: everyone may experience more serious health effects. Avoid outdoor activities."
        else:
            return "Health warning of emergency conditions. The entire population is likely to be affected. Stay indoors!"
    
    def perceive_and_act(self, sensor_data):
        """Main perception-action cycle of the reflex agent.
        
        Args:
            sensor_data: Dictionary containing pollutant concentrations
                        Keys: 'pm25', 'pm10', 'o3', 'co', 'no2'
                        
        Returns:
            Dictionary with AQI information and recommendations
        """
        # Calculate individual AQI for each pollutant
        individual_aqis = {}
        
        if 'pm25' in sensor_data:
            individual_aqis['PM2.5'] = self.calculate_individual_aqi(
                sensor_data['pm25'], self.pm25_breakpoints
            )
        
        if 'pm10' in sensor_data:
            individual_aqis['PM10'] = self.calculate_individual_aqi(
                sensor_data['pm10'], self.pm10_breakpoints
            )
        
        if 'o3' in sensor_data:
            individual_aqis['O3'] = self.calculate_individual_aqi(
                sensor_data['o3'], self.o3_breakpoints
            )
        
        if 'co' in sensor_data:
            individual_aqis['CO'] = self.calculate_individual_aqi(
                sensor_data['co'], self.co_breakpoints
            )
        
        if 'no2' in sensor_data:
            individual_aqis['NO2'] = self.calculate_individual_aqi(
                sensor_data['no2'], self.no2_breakpoints
            )
        
        # Overall AQI is the maximum of individual AQIs
        overall_aqi = max(individual_aqis.values()) if individual_aqis else 0
        dominant_pollutant = max(individual_aqis, key=individual_aqis.get) if individual_aqis else "None"
        
        # Get category and recommendations
        category = self.get_aqi_category(overall_aqi)
        recommendations = self.get_health_recommendations(overall_aqi)
        
        # Return the agent's response
        return {
            'overall_aqi': overall_aqi,
            'category': category,
            'dominant_pollutant': dominant_pollutant,
            'individual_aqis': individual_aqis,
            'health_recommendations': recommendations,
            'sensor_readings': sensor_data
        }


def simulate_sensor_readings():
    """Simulate various sensor reading scenarios for demonstration."""
    scenarios = [
        {
            'name': 'Good Air Quality',
            'data': {'pm25': 8.0, 'pm10': 30, 'o3': 0.040, 'co': 2.0, 'no2': 25}
        },
        {
            'name': 'Moderate Air Quality',
            'data': {'pm25': 25.0, 'pm10': 85, 'o3': 0.065, 'co': 5.5, 'no2': 75}
        },
        {
            'name': 'Unhealthy for Sensitive Groups',
            'data': {'pm25': 45.0, 'pm10': 200, 'o3': 0.078, 'co': 10.5, 'no2': 150}
        },
        {
            'name': 'Unhealthy Air Quality',
            'data': {'pm25': 95.0, 'pm10': 280, 'o3': 0.095, 'co': 13.0, 'no2': 500}
        },
        {
            'name': 'Very Unhealthy Air Quality',
            'data': {'pm25': 185.0, 'pm10': 380, 'o3': 0.150, 'co': 20.0, 'no2': 900}
        },
        {
            'name': 'Hazardous Air Quality',
            'data': {'pm25': 305.0, 'pm10': 500, 'o3': 0.190, 'co': 35.0, 'no2': 1500}
        }
    ]
    
    return scenarios


def main():
    """Main function to demonstrate the AQI Reflex Agent."""
    print("=" * 80)
    print("Simple Reflex Agent for Air Quality Index (AQI) Calculation")
    print("=" * 80)
    print()
    
    # Create the reflex agent
    agent = AQIReflexAgent()
    
    # Get simulated scenarios
    scenarios = simulate_sensor_readings()
    
    # Process each scenario
    for scenario in scenarios:
        print(f"\nScenario: {scenario['name']}")
        print("-" * 80)
        print("\nSensor Readings:")
        for pollutant, value in scenario['data'].items():
            print(f"  {pollutant.upper()}: {value}")
        
        # Agent perceives and acts
        result = agent.perceive_and_act(scenario['data'])
        
        print(f"\nAgent Response:")
        print(f"  Overall AQI: {result['overall_aqi']}")
        print(f"  Category: {result['category']}")
        print(f"  Dominant Pollutant: {result['dominant_pollutant']}")
        print(f"\nIndividual AQI Values:")
        for pollutant, aqi in result['individual_aqis'].items():
            print(f"  {pollutant}: {aqi}")
        print(f"\nHealth Recommendations:")
        print(f"  {result['health_recommendations']}")
        print()
    
    # Interactive mode
    print("\n" + "=" * 80)
    print("Interactive Mode: Enter your own sensor readings")
    print("=" * 80)
    print("\nEnter sensor data (press Enter to skip a pollutant):")
    
    try:
        sensor_data = {}
        
        pm25 = input("PM2.5 concentration (µg/m³): ").strip()
        if pm25:
            sensor_data['pm25'] = float(pm25)
        
        pm10 = input("PM10 concentration (µg/m³): ").strip()
        if pm10:
            sensor_data['pm10'] = float(pm10)
        
        o3 = input("O3 concentration (ppm): ").strip()
        if o3:
            sensor_data['o3'] = float(o3)
        
        co = input("CO concentration (ppm): ").strip()
        if co:
            sensor_data['co'] = float(co)
        
        no2 = input("NO2 concentration (ppb): ").strip()
        if no2:
            sensor_data['no2'] = float(no2)
        
        if sensor_data:
            print("\n" + "-" * 80)
            result = agent.perceive_and_act(sensor_data)
            print(f"\nAgent Response:")
            print(f"  Overall AQI: {result['overall_aqi']}")
            print(f"  Category: {result['category']}")
            print(f"  Dominant Pollutant: {result['dominant_pollutant']}")
            print(f"\nIndividual AQI Values:")
            for pollutant, aqi in result['individual_aqis'].items():
                print(f"  {pollutant}: {aqi}")
            print(f"\nHealth Recommendations:")
            print(f"  {result['health_recommendations']}")
        else:
            print("\nNo sensor data provided.")
    
    except ValueError:
        print("\nInvalid input. Please enter numeric values.")
    except KeyboardInterrupt:
        print("\n\nExiting interactive mode.")


if __name__ == "__main__":
    main()
