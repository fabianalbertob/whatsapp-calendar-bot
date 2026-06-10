if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando WhatsApp Calendar Bot en modo debug...")
    
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8080, 
        log_level="debug"
    )