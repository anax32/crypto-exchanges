from fluent/fluentd

run apk --no-cache --update add \
                            build-base \
                            ruby-dev && \
    fluent-gem install fluent-plugin-mongo && \
    apk del build-base ruby-dev && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/*
