# 🔧 Troubleshooting Guide

## Problem: "localhost:8050 can't be reached"

### **Quick Fix**

#### **Option 1: Use the Startup Script (Easiest)**
1. Double-click `start_bloomberg_terminal.bat`
2. Wait for packages to install (first time only)
3. Browser should open automatically to http://localhost:8050

#### **Option 2: Manual Start**
```bash
# Open Command Prompt in the agentspoons folder
cd "d:\Agentic Spoons\agentspoons"

# Install packages (first time only)
py -m pip install dash plotly dash-bootstrap-components numpy

# Start the terminal
py src\bloomberg_terminal.py
```

#### **Option 3: Use Alternative Dashboard**
If Bloomberg Terminal has issues, try the championship dashboard:
```bash
py src\championship_dashboard.py
```

---

## Common Issues & Solutions

### **Issue 1: Python Not Found**

**Symptom:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
```bash
# Use 'py' instead of 'python' on Windows
py --version

# If that doesn't work, install Python:
# Download from: https://www.python.org/downloads/
# Check "Add Python to PATH" during installation
```

---

### **Issue 2: Module Not Found (dash, plotly, etc.)**

**Symptom:**
```
ModuleNotFoundError: No module named 'dash'
```

**Solution:**
```bash
# Install required packages
py -m pip install dash plotly dash-bootstrap-components numpy

# Or install everything from requirements
py -m pip install -r requirements.txt
```

---

### **Issue 3: Port 8050 Already in Use**

**Symptom:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**

**Option A: Kill the existing process**
```bash
# Windows
netstat -ano | findstr :8050
taskkill /PID <PID_NUMBER> /F

# Find the PID from netstat output, then kill it
```

**Option B: Use a different port**
Edit the last line in `src\bloomberg_terminal.py`:
```python
# Change from port 8050 to 8051
app.run(debug=True, host='0.0.0.0', port=8051)
```

Then visit: http://localhost:8051

---

### **Issue 4: Import Error (themes.py)**

**Symptom:**
```
ModuleNotFoundError: No module named 'dashboard.themes'
```

**Solution:**
The path might not be set correctly. Edit `src\bloomberg_terminal.py`:

```python
# Add this at the top of the file
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

---

### **Issue 5: Blank Page / No Data**

**Symptom:**
Page loads but shows "Waiting for data..." or empty panels

**Cause:**
The terminal generates sample data, so this shouldn't happen. But if it does:

**Solution:**
1. Check browser console (F12) for errors
2. Verify the terminal is running (check Command Prompt window)
3. Refresh the page (Ctrl+F5)
4. Check if data/results.json exists (for championship dashboard)

---

### **Issue 6: Firewall Blocking**

**Symptom:**
Can't connect even though server is running

**Solution:**
1. Check Windows Firewall settings
2. Allow Python through firewall
3. Try accessing from: http://127.0.0.1:8050 instead of localhost

---

### **Issue 7: Browser Compatibility**

**Symptom:**
Terminal doesn't display correctly

**Solution:**
- Use **Chrome** or **Edge** (recommended)
- Update browser to latest version
- Clear browser cache
- Disable browser extensions

---

## Step-by-Step Troubleshooting

### **1. Verify Python Installation**
```bash
py --version
# Should show: Python 3.10 or higher
```

### **2. Check Package Installation**
```bash
py -c "import dash; print('dash:', dash.__version__)"
py -c "import plotly; print('plotly:', plotly.__version__)"
```

### **3. Test Simple Dash App**
Create `test_dash.py`:
```python
import dash
from dash import html

app = dash.Dash(__name__)
app.layout = html.Div("Hello Dash!")

if __name__ == '__main__':
    print("Starting test server on http://localhost:8050")
    app.run(debug=True, port=8050)
```

Run it:
```bash
py test_dash.py
```

If this works, the issue is with the Bloomberg Terminal code.

### **4. Check Terminal Startup**
Look for this output when starting:
```
================================================================================
🥄 AGENTSPOONS BLOOMBERG TERMINAL
================================================================================
URL: http://localhost:8050
Features:
  • Professional Bloomberg-style interface
  • Real-time market data & volatility tracking
  ...
================================================================================

Dash is running on http://0.0.0.0:8050/

 * Serving Flask app 'bloomberg_terminal'
 * Debug mode: on
```

### **5. Test Network Connection**
```bash
# Check if port is listening
netstat -an | findstr 8050

# Should show something like:
# TCP    0.0.0.0:8050    0.0.0.0:0    LISTENING
```

---

## Alternative Dashboards

If Bloomberg Terminal won't start, try these alternatives:

### **Championship Dashboard** (Recommended)
```bash
py src\championship_dashboard.py
```
- URL: http://localhost:8050
- Has dark/light theme toggle
- All volatility features

### **Simple Bloomberg Layout**
```bash
py src\dashboard\bloomberg_layout.py
```
- URL: http://localhost:8060
- Simpler version
- Should work if main terminal fails

### **Analytics Dashboard**
```bash
py src\dashboard\analytics_dashboard.py
```
- Full analytics suite
- Different port (check console output)

---

## Windows-Specific Issues

### **Antivirus Blocking**
Some antivirus software blocks Python from opening network ports.

**Solution:**
- Add Python to antivirus exceptions
- Temporarily disable antivirus to test

### **PATH Issues**
Python might not be in your system PATH.

**Solution:**
Use full path:
```bash
C:\Users\LENOVO\AppData\Local\Programs\Python\Python312\python.exe src\bloomberg_terminal.py
```

### **File Permissions**
Running from a protected directory (like Program Files).

**Solution:**
- Move project to Documents or Desktop
- Run Command Prompt as Administrator

---

## Getting Detailed Error Information

### **Enable Debug Mode**
In `src\bloomberg_terminal.py`, ensure:
```python
app.run(debug=True, host='0.0.0.0', port=8050)
#       ^^^^^^^^^^^
```

### **Check Console Output**
Look for error messages in the Command Prompt window where you started the server.

### **Browser Developer Tools**
1. Press F12 in browser
2. Go to Console tab
3. Look for JavaScript errors
4. Go to Network tab
5. Check for failed requests

---

## Still Not Working?

### **Manual Installation Steps**

1. **Fresh Python Environment**
```bash
# Create virtual environment
py -m venv venv

# Activate it
venv\Scripts\activate

# Install packages
pip install dash plotly dash-bootstrap-components numpy
```

2. **Minimal Test**
Create `minimal_terminal.py`:
```python
import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AgentSpoons Terminal - Minimal Test"),
    html.P("If you see this, Dash is working!")
], style={'backgroundColor': '#000000', 'color': '#ff8c00', 'padding': '20px'})

if __name__ == '__main__':
    print("\nTest server running on http://localhost:8050\n")
    app.run(debug=True, port=8050)
```

Run it:
```bash
py minimal_terminal.py
```

If this works, gradually add features from bloomberg_terminal.py.

---

## Quick Checklist

- [ ] Python 3.10+ installed
- [ ] `py --version` works
- [ ] Dash installed (`py -m pip install dash`)
- [ ] Plotly installed (`py -m pip install plotly`)
- [ ] Port 8050 is free (not used by other app)
- [ ] Firewall allows Python
- [ ] Using Chrome or Edge browser
- [ ] Running from correct directory

---

## Emergency Fallback

If nothing works, use the simplest version:

```bash
# Install minimal requirements
py -m pip install dash plotly numpy

# Run the original championship dashboard (should be stable)
py src\championship_dashboard.py
```

This should always work as it's the original tested code.

---

## Contact for Help

If you've tried everything above:

1. Note the exact error message
2. Note your Python version (`py --version`)
3. Note installed packages (`py -m pip list`)
4. Check the error in Command Prompt
5. Check browser console (F12) for errors

---

## Success Indicators

You know it's working when you see:

### **In Command Prompt:**
```
================================================================================
🥄 AGENTSPOONS BLOOMBERG TERMINAL
================================================================================
Dash is running on http://0.0.0.0:8050/
```

### **In Browser:**
- Orange top bar with "🥄 AGENTSPOONS TERMINAL"
- Command line with ">" prompt
- Three-column layout
- Black background with orange highlights
- Live clock ticking in top right

---

## Performance Tips

Once it's running:

- **Chrome/Edge recommended** - Best performance
- **Close other browser tabs** - Reduce memory usage
- **Disable browser extensions** - Avoid conflicts
- **Use wired connection** - Better than WiFi
- **Keep Command Prompt open** - Don't close it while using terminal

---

**Good luck! The terminal is worth the troubleshooting!** 🟠
