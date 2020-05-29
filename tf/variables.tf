variable "aws_access_key_id" {
  type = string
}

variable "aws_secret_access_key" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "aws_availability_zones" {
  type    = list(string)
  default = ["europe-west-2-a"]
}

variable "whitelist_ips" {
  type = list(string)
}

variable "public_key" {
  type = map(string)
}

variable "default_tags" {
  type = map
  default = {
    project = "btc.exchanges"
    mode    = "infrastructure"
  }
}
