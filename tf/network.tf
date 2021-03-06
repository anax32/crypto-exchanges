resource "aws_vpc" "default" {
  cidr_block = "10.10.0.0/16"

  enable_dns_hostnames = true

  tags = merge(var.default_tags,
               {Name = "btc.exchanges.vpc"})
}

resource "aws_subnet" "public" {
  vpc_id = aws_vpc.default.id
  cidr_block = "10.10.1.0/24"
  map_public_ip_on_launch = true

  tags = merge(var.default_tags,
               {Name = "btc.exchanges.subnet"})
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.default.id

  tags = merge(var.default_tags,
               {Name = "btc.exchanges.igw"})
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.default.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = merge(var.default_tags,
               {Name = "btc.exchanges.route_table"})
}

resource "aws_route_table_association" "default" {
  subnet_id = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "default" {
  name_prefix = "btc.exchanges.sg"
  vpc_id      = aws_vpc.default.id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = var.whitelist_ips
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.default_tags,
               {Name = "btc.exchanges.sg"})
}
