# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libasound2 \
    libxrandr2 \
    libatk1.0-0 \
    libgtk-3-0 \
    libxss1 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils

# Download and install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -yf

# Download and install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) && \
    wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION} -O /tmp/chromedriver_version && \
    CHROMEDRIVER_VERSION=$(cat /tmp/chromedriver_version) && \
    wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -O /tmp/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver
