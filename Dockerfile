FROM nikolaik/python-nodejs:python3.8-nodejs12

WORKDIR /app
RUN mkdir /app/data
COPY req.txt .
COPY package.json .
COPY package-lock.json .
RUN pip install --no-cache-dir -r req.txt
RUN npm install
COPY . .
RUN npm run build
CMD [ "python", "/app/server/bettor.py" ]
