# Contract Generation System - User Manual

## 1. Introduction
The Contract Generation System is an AI-powered tool for automated contract creation, designed to help users quickly generate legally compliant contract documents. This system combines natural language processing, legal knowledge graphs, and document template technology to provide contract template recommendations, intelligent information extraction, and automatic document generation.

## 2. System Requirements
- Operating System: Windows 10/11
- Python Version: 3.9.21
- Dependencies: See environment.yml in the project root directory
- Hardware: Minimum 8GB RAM, 16GB recommended for optimal performance

## 3. Installation and Startup

### 3.1 Environment Setup
1. Ensure Anaconda or Miniconda is installed
2. Open Command Prompt and navigate to the project root directory
3. Execute the following commands to create and activate the environment:
   ```
   conda env create -f demo/environment.yml
   conda activate contract_generator
   ```

### 3.2 Launching the Application
1. After activating the environment, run the following commands to start the system:
   ```
   cd demo
   python demo.py
   ```
2. The system will launch a graphical user interface displaying the main operation window

## 4. User Interface Overview

### 4.1 Main Interface Layout
- **Contract Type Selection Area**: Located on the left, displaying selectable contract categories
- **Template Selection Area**: In the middle, showing available templates based on selected contract type
- **Description Input Area**: At the top, for entering contract-related information and special requirements
- **Operation Buttons Area**: At the bottom, containing functional buttons like "Recommend Templates" and "Generate Contract"
- **Log and Progress Area**: On the right, showing system status and progress
- **Results Display Area**: At the bottom, showing generated contract list

### 4.2 Main Components
- **Contract Type Dropdown**: Select contract category (e.g., sales contracts, rental contracts)
- **Template List**: Displays available templates for the selected contract type
- **Description Text Box**: Enter specific contract requirements and special clauses
- **Progress Bar**: Shows the progress of the contract generation process
- **Log Window**: Displays detailed system operation logs
- **Results Table**: Shows information about generated contract files

## 5. Usage Workflow

### 5.1 Basic Operation Steps
1. **Select Contract Type**: Choose the desired contract type from the left dropdown menu
2. **Enter Contract Description**: Detail the specific content, party information, and special requirements in the text box
3. **Get Template Recommendations**: Click the "Recommend Templates" button, and the system will recommend suitable templates based on your description
4. **Select Template**: Choose the most appropriate template from the recommended list
5. **Generate Contract**: Click the "Generate Contract" button, and the system will automatically generate a complete contract document
6. **View Results**: Find the generated contract in the results table and click the "Open" button to view it

### 5.2 Advanced Features
- **Custom Templates**: Add custom templates to the contracts/template directory, which the system will automatically recognize
- **Contract Management**: Rename, delete, and export contracts in the generated contract list
- **Parameter Adjustment**: Adjust generation parameters like similarity threshold and output length through the "Settings" button

## 6. Troubleshooting

### 6.1 Common Issues
- **Application fails to start**: Check if the Python environment is properly activated and dependencies are fully installed
- **Inaccurate template recommendations**: Provide more detailed contract descriptions or manually select appropriate templates
- **Contract generation fails**: Check network connection (requires internet access for AI model calls) or reduce input text length
- **Chinese display garbled**: Ensure system encoding is UTF-8 and font settings are correct
