# 降低内存占用
unicorn['worker_processes'] = 2
postgresql['shared_buffers'] = "128MB"
postgresql['max_worker_processes'] = 8
sidekiq['concurrency'] = 10

# 使用https访问
external_url "https://gitlab.zkeli.com"
nginx['enable'] = true
nginx['client_max_body_size'] = '1024m'
nginx['redirect_http_to_https'] = true
nginx['redirect_http_to_https_port'] = 80
nginx['ssl_certificate'] = "/etc/gitlab/ssl/gitlab.zkeli.com.crt"
nginx['ssl_certificate_key'] = "/etc/gitlab/ssl/gitlab.zkeli.com.key"
#
#
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.qq.com"
gitlab_rails['smtp_port'] = 465
gitlab_rails['smtp_user_name'] = "528752273@qq.com"
gitlab_rails['smtp_password'] = "igcmwxnxhllhbgfj"   #开启qq的POP3时得到的密码
gitlab_rails['smtp_domain'] = "smtp.qq.com"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = true
gitlab_rails['smtp_tls'] = true
gitlab_rails['gitlab_email_from'] = '528752273@qq.com'