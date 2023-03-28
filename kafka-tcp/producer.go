package main

import (
	"fmt"
	"io"
	"net"
	"os"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

func getproducer() *kafka.Producer {

	producer, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": os.Getenv("BOOTSTRAP_SERVER"),
	})
	if err != nil {
		panic(err)
	}
	return producer
}

func main() {
	port := os.Args[1]
	listener, err := net.Listen("tcp", fmt.Sprintf(":%s", port))

	if err != nil {
		fmt.Printf("fail to bind address: %v", err)
	}
	defer listener.Close()
	producer := getproducer()

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Printf("연결 실패: %v", err)
			continue
		} else {
			fmt.Printf("클라이언트 연결: %v", conn.RemoteAddr())
		}
		go sender(conn, producer, port)
		go asynchandler(producer)
	}
}

func sender(conn net.Conn, producer *kafka.Producer, topic string) {

	recvBuf := make([]byte, 4096)
	delivery_chan := make(chan kafka.Event, 10000)

	for {
		cnt, err := conn.Read(recvBuf)
		if err != nil {
			if io.EOF == err {
				fmt.Printf("연결 종료: %v", conn.RemoteAddr().String())
			} else {
				fmt.Printf("수신 실패: %v", err)
			}
			return
		}
		if cnt > 0 {
			data := recvBuf[:cnt]
			err = producer.Produce(&kafka.Message{
				TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
				Value:          []byte(data)},
				delivery_chan,
			)
		}
	}
}

func asynchandler(producer *kafka.Producer) {
	for e := range producer.Events() {
		switch ev := e.(type) {
		case *kafka.Message:
			if ev.TopicPartition.Error != nil {
				fmt.Printf("Failed to deliver message: %v\n", ev.TopicPartition)
			} else {
				fmt.Printf("Successfully produced record to topic %s partition [%d] @ offset %v\n", *ev.TopicPartition.Topic, ev.TopicPartition.Partition, ev.TopicPartition.Offset)
			}
		}
	}
}
