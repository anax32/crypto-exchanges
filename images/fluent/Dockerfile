from fluent/fluentd

run apk --no-cache --update add \
                            build-base \
                            ruby-dev && \
    fluent-gem install fluent-plugin-mongo && \
    fluent-gem install fluent-plugin-s3 && \
    apk del build-base ruby-dev && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/*
