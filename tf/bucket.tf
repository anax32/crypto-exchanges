data "aws_s3_bucket" "output" {
  bucket = var.aws_s3_output_name
}
