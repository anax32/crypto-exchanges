resource "aws_key_pair" "key" {
  key_name = var.public_key.name
  public_key = var.public_key.ssh
}

resource "aws_iam_role" "default" {
  name = "ec2-role"
  assume_role_policy = file("policies/ec2-assume-role.json")
  tags = var.default_tags
}

resource "aws_iam_instance_profile" "default" {
  name = "ec2-profile"
  role = aws_iam_role.default.name
}

resource "aws_iam_role_policy" "default" {
  name = "ec2-s3-access"
  role = aws_iam_role.default.id
  policy = file("policies/s3-access.json")
}

resource "aws_instance" "instance" {
  ami = "ami-006a0174c6c25ac06"
  instance_type = "t2.micro"
  iam_instance_profile = aws_iam_instance_profile.default.name

  vpc_security_group_ids = [aws_security_group.default.id]
  subnet_id = aws_subnet.public.id

  user_data = file("scripts/vm-startup.sh")

  key_name = aws_key_pair.key.key_name

  tags = merge(var.default_tags,
               {Name = "btc.exchanges.instance"})
}

resource "aws_s3_bucket" "s3_upload_bucket" {
  bucket = "exchanges.btc.bayis.co.uk"
  region = var.aws_region

  tags = merge(var.default_tags,
               {Name = "btc.exchanges.storage"})
}

output "instance_public_dns" {
  value = aws_instance.instance.public_dns
}

output "instance_public_ip" {
  value = aws_instance.instance.public_ip
}
