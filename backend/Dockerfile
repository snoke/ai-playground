FROM php:8.3-fpm

RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libicu-dev \
    libxml2-dev \
    libzip-dev \
    libgmp-dev \
    unzip \
    git \
    libonig-dev \
    openssh-server \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd pdo pdo_mysql intl xml zip opcache gmp

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

ENV COMPOSER_ALLOW_SUPERUSER=1

RUN curl -sS https://get.symfony.com/cli/installer | bash \
    && mv /root/.symfony*/bin/symfony /usr/local/bin/symfony

WORKDIR /var/www/html

COPY . .

RUN chown -R www-data:www-data /var/www
RUN chown -R www-data:www-data /var/www/html

# SSH-Konfiguration
RUN mkdir /var/run/sshd
RUN useradd -ms /bin/bash phpstorm_user
RUN echo 'phpstorm_user:password' | chpasswd
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config

EXPOSE 22 9001

CMD ["bash", "-c", "service ssh start  && php-fpm & \
    php -S 0.0.0.0:9001 -t public"  ]

