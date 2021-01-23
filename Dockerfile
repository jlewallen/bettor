FROM nikolaik/python-nodejs:python3.8-nodejs12

WORKDIR /app

COPY requirements.txt .
COPY package.json .
COPY package-lock.json .
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install
COPY . .
RUN npm run build
RUN mv dist static
CMD [ "python", "/app/server/bettor.py" ]
