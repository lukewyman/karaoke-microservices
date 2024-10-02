###################
# DynamoDB Tables #
###################

resource "aws_dynamodb_table" "queues" {
    name = "${local.app_prefix}-queues"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "queue_id"

    attribute {
      name = "queue_id"
      type = "S"
    }
}

resource "aws_dynamodb_table" "enqueued_singers" {
    name = "${local.app_prefix}-enqueued-singers"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "queue_id"
    range_key = "queue_position"

    attribute {
      name = "queue_id"
      type = "S"
    }

    attribute {
      name = "queue_position"
      type = "N"
    }
}

resource "aws_dynamodb_table" "song_choices" {
    name = "${local.app_prefix}-song-choices"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "enqueued_singer_id"
    range_key = "position"

    attribute {
      name = "enqueued_singer_id"
      type = "S"
    }

    attribute {
      name = "position"
      type = "N"
    }
}


##############
# S3 BUCKETS #
##############

# Bucket for karaoke tracks for song-library will go here.