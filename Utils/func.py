# Scaling function
def min_max_scaling(df):
    """Applies Min-Max scaling using predefined min/max values from the training data."""
    
    min_vals = {
    'Mach': 0.23, 'Fuel Flow': 2808.00, 'Vibration N1 #1 Bearing': 0.07, 'Vibration N2 #1 Bearing': 0.00,
    'Oil Temperature': 67.00, 'EGT': 716.90, 'Total Air Temperature': 7.30, 'Oil Pressure': 52.00,
    'Oil Pressure Smoothed': 54.76, 'Altitude': 0.00, 'Indicated Fan Speed': 85.94,
    'Thrust Derate': -4.32, 'Thrust Derate Smoothed': 2.09, 'Core Speed': 94.30,
    'Oil Temperature Smoothed': 78.72, 'DAYS_SINCE_INSTALL': 138.00}

    max_vals = {
    'Mach': 0.35, 'Fuel Flow': 10931.00, 'Vibration N1 #1 Bearing': 1.46, 'Vibration N2 #1 Bearing': 0.28,
    'Oil Temperature': 108.00, 'EGT': 924.00, 'Total Air Temperature': 44.50, 'Oil Pressure': 62.51,
    'Oil Pressure Smoothed': 60.66, 'Altitude': 9176.00, 'Indicated Fan Speed': 102.50,
    'Thrust Derate': 36.62, 'Thrust Derate Smoothed': 21.65, 'Core Speed': 101.27,
    'Oil Temperature Smoothed': 94.75, 'DAYS_SINCE_INSTALL': 3096.82}
    
    df_scaled = df.copy()
    
    for col in df.select_dtypes(include=['number']).columns:
        if col in min_vals and col in max_vals:
            X_min, X_max = min_vals[col], max_vals[col]
            if X_max != X_min:  # Prevent division by zero
                df_scaled[col] = (df[col] - X_min) / (X_max - X_min)
            else:
                df_scaled[col] = 0  # If min and max are the same, set scaled value to 0
    
    return df_scaled
    

#Unscaling function
def inverse_min_max_scaling(y_scaled, y_min=18.99, y_max=92.27):
    """
    Restores a Min-Max scaled prediction to its original scale.

    Parameters:
    y_scaled (float or array-like): The scaled prediction(s) from the model.
    y_min (float): The minimum value of the target variable from training data.
    y_max (float): The maximum value of the target variable from training data.

    Returns:
    float or array-like: The unscaled prediction(s).
    """
    return y_scaled * (y_max - y_min) + y_min