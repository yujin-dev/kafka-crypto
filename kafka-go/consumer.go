package main

import (
	"fmt"
	"os"
	"time"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

func getconsumer() *kafka.Consumer {

	consumer, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": os.Getenv("BOOTSTRAP_SERVER"),
		"group.id":          "my-consumer",
		"auto.offset.reset": "earliest",
	})
	if err != nil {
		panic(err)
	}
	return consumer
}

func main() {
	consumer := getconsumer()
	port := os.Args[1]
	topics := []string{port}
	consumer.SubscribeTopics(topics, nil)
	asynchandler(consumer)
	consumer.Close()
}

func basichandler(consumer *kafka.Consumer) {
	run := true

	for run == true {
		ev := consumer.Poll(10)
		switch e := ev.(type) {
		case *kafka.Message:
			now := time.Now()
			fmt.Printf("%v [ Received ] %s : %s", now, e.TopicPartition, string(e.Value))
		case kafka.PartitionEOF:
			fmt.Printf("[ Reached ] %v", e)
		case kafka.Error:
			fmt.Fprintf(os.Stderr, "[ Error ] %v", e)
			run = false
		}
	}
}

func asynchandler(consumer *kafka.Consumer) {
	run := true
	msg_count := 0

	for run == true {
		ev := consumer.Poll(10)
		switch e := ev.(type) {
		case *kafka.Message:
			msg_count += 1
			go func() {
				offsets, err := consumer.Commit()
				if err != nil {
					fmt.Printf("[ Error ] %v", err)
					os.Exit(1)
				} else {
					record_time := time.Now()
					fmt.Printf("%v [ Record ] %v", record_time, offsets)
				}
			}()
			now := time.Now()
			fmt.Printf("%v [ Received ] %s : %s", now, e.TopicPartition, string(e.Value))
		case kafka.PartitionEOF:
			fmt.Printf("[ Reached ] %v", e)
		case kafka.Error:
			fmt.Fprintf(os.Stderr, "[ Error ] %v", e)
			run = false
		}
	}
}
