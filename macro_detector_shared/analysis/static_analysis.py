from oletools.olevba import VBA_Parser

def analyze_vba_macros(file_path):
    """
    Performs static analysis on a Word document to extract and inspect VBA macros.

    Returns:
        dict: {
            "vba_code": str,                  # Extracted macro code (or explanation)
            "suspicious_keywords": list[str]  # Matched risky terms like Shell, WScript, etc.
        }
    """
    result = {
        "vba_code": "",
        "suspicious_keywords": []
    }

    # Common indicators of malicious intent
    suspicious_keywords = [
        "Shell", "CreateObject", "WScript", "Run", "Execute", "cmd.exe", "PowerShell",
        "AutoOpen", "Document_Open", "Kill", "Environ", "Base64Decode", "ChrW", "Hex"
    ]

    try:
        # Initialize parser
        vbaparser = VBA_Parser(file_path)

        if vbaparser.detect_vba_macros():
            all_macros = ""

            for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
                all_macros += f"\n\n--- Macro from {vba_filename} ---\n{vba_code}"

            result["vba_code"] = all_macros.strip()

            # Lowercase for easier matching
            lowered_code = all_macros.lower()

            for keyword in suspicious_keywords:
                if keyword.lower() in lowered_code:
                    result["suspicious_keywords"].append(keyword)

        else:
            result["vba_code"] = "No VBA macros were detected in the document."

    except Exception as e:
        result["vba_code"] = f"Error analyzing macros: {str(e)}"

    return result
