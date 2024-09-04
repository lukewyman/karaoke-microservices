output "queues_table_name" {
    value = aws_dynamodb_table.queues.name
}

output "enqueued_singers_table_name" {
    value = aws_dynamodb_table.enqueued_singers.name 
}

output "song_choices_table_name" {
    value = aws_dynamodb_table.song_choices.name 
}