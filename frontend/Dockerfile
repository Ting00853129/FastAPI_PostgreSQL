# # Base image
# FROM node:alpine

# # Create app directory
# WORKDIR /root

# # Install app dependencies
# COPY package.json /root
# RUN yarn install && yarn cache clean

# #Bundle app source
# COPY . /root

# EXPOSE 8080

# CMD ["yarn", "start"]
FROM httpd:2.4
COPY ./ /usr/local/apache2/htdocs/