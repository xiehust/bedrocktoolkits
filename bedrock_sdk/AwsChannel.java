// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: Apache-2.0

package com.ke.gpt.channel.completion.channel.aws;

// snippet-start:[bedrock-runtime.java2.InvokeModel_AnthropicClaude]
// Use the native inference API to send a text message to Anthropic Claude.

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Base64;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

import com.ke.gpt.channel.utils.json.JacksonUtils;

import lombok.Data;
import software.amazon.awssdk.core.document.Document;
import software.amazon.awssdk.core.exception.SdkClientException;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeAsyncClient;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;
import software.amazon.awssdk.services.bedrockruntime.model.ContentBlock;
import software.amazon.awssdk.services.bedrockruntime.model.ContentBlockStart;
import software.amazon.awssdk.services.bedrockruntime.model.ConversationRole;
import software.amazon.awssdk.services.bedrockruntime.model.ConverseResponse;
import software.amazon.awssdk.services.bedrockruntime.model.ConverseStreamRequest;
import software.amazon.awssdk.services.bedrockruntime.model.ConverseStreamResponseHandler;
import software.amazon.awssdk.services.bedrockruntime.model.InferenceConfiguration;
import software.amazon.awssdk.services.bedrockruntime.model.Message;
import software.amazon.awssdk.services.bedrockruntime.model.SystemContentBlock;
import software.amazon.awssdk.services.bedrockruntime.model.Tool;
import software.amazon.awssdk.services.bedrockruntime.model.ToolConfiguration;
import software.amazon.awssdk.services.bedrockruntime.model.ToolInputSchema;
import software.amazon.awssdk.services.bedrockruntime.model.ToolResultBlock;
import software.amazon.awssdk.services.bedrockruntime.model.ToolResultContentBlock;

@RunWith(JUnit4.class)
public class AwsChannel {

    @Test
    public void converse() {
        String schema = "{\"type\":\"object\",\"properties\":{\"latitude\":{\"type\":\"string\",\"description\":\"纬度\"},\"longitude\":{\"type\":\"string\",\"description\":\"经度\"}},\"required\":[\"latitude\",\"longitude\"]}";
        Map schemaMap = JacksonUtils.deserialize(schema, Map.class);

        // Create a Bedrock Runtime client in the AWS Region you want to use.
        // Replace the DefaultCredentialsProvider with your preferred
        // credentials provider.
        BedrockRuntimeClient client = BedrockRuntimeClient.builder()
                .credentialsProvider(FixedPropertyCredentialsProvider.create())
                .region(Region.US_EAST_1)
                .build();

        String modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0";

        // Create the input text and embed it in a message object with the user
        // role.
        // String inputText = "描述一下这个图片";
        String base64String = "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"; // 示例base64字符串
        byte[] decodedBytes = Base64.getDecoder().decode(base64String);
//        ContentBlock contentBlock = ContentBlock.builder()
//                .image(ImageBlock.builder()
//                        .format("png")
//                        .source(ImageSource.builder()
//                                .bytes(SdkBytes.fromByteArray(decodedBytes))
//                                .build())
//                        .build())
//                .build();
        software.amazon.awssdk.services.bedrockruntime.model.ToolSpecification.Builder toolBuilder = software.amazon.awssdk.services.bedrockruntime.model.ToolSpecification
                .builder();
        toolBuilder.name("queryWeather");
        toolBuilder.description("queryWeather");
        toolBuilder.inputSchema(ToolInputSchema.builder().json(convertObjectToDocument(schemaMap)).build());
        Tool tool = Tool.fromToolSpec(toolBuilder.build());
        String inputText = "查一下，北纬60度东经110度的天气";
        String inputText2 = "这个天气怎么样";
        ContentBlock contentBlock = ContentBlock.builder()
                .text(inputText2).build();

        ContentBlock contentBlock2 = ContentBlock.builder()
                .toolResult(ToolResultBlock
                        .builder()
                        .content(ToolResultContentBlock.fromText("30摄氏度"))
                        .toolUseId("tooluse_ZImM8gzPRvqzAnlDxyyW5Q")
                        .build())
                .build();
        Message message = Message.builder()
                .content(contentBlock)
                .role(ConversationRole.ASSISTANT)
                .build();
        Message message2 = Message.builder()
                .content([contentBlock2])
                .role(ConversationRole.USER)
                .build();

        try {
            // Send the message with a basic inference configuration.
            ConverseResponse response = client.converse(request -> request
                    .modelId(modelId)
                    .system(SystemContentBlock.builder().text("你是一个气象小助手").build(), SystemContentBlock.builder().text("你是一个气象小助手").build())
                    .messages(message2)
                    .toolConfig(ToolConfiguration.builder().tools(tool).build())
                    .inferenceConfig(config -> config
                            .maxTokens(512)
                            .temperature(0.5F)
                            .topP(0.9F)));

            // Retrieve the generated text from Bedrock's response object.
            String responseText = response.output().message().content().get(0).text();
            System.out.println(responseText);

        } catch (SdkClientException e) {
            System.out.printf("ERROR: Can't invoke '%s'. Reason: %s%n", modelId, e.getMessage());
            throw new RuntimeException(e);
        }
    }

    @Test
    public void converseStream() {
        String schema = "{\"type\":\"object\",\"properties\":{\"latitude\":{\"type\":\"string\",\"description\":\"纬度\"},\"longitude\":{\"type\":\"string\",\"description\":\"经度\"}},\"required\":[\"latitude\",\"longitude\"]}";
        Map schemaMap = JacksonUtils.deserialize(schema, Map.class);

        // Create a Bedrock Runtime client in the AWS Region you want to use.
        // Replace the DefaultCredentialsProvider with your preferred
        // credentials provider.
        BedrockRuntimeAsyncClient client = BedrockRuntimeAsyncClient.builder()
                .credentialsProvider(FixedPropertyCredentialsProvider.create())
                .region(Region.US_EAST_1)
                .build();

        String modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0";
        StringBuilder sb = new StringBuilder();
        ConverseStreamResponseHandler responseStreamHandler = ConverseStreamResponseHandler.builder()
                .subscriber(ConverseStreamResponseHandler.Visitor.builder()
                        .onContentBlockStart(chunk -> {
                            System.out.print(chunk.contentBlockIndex());
                            ContentBlockStart start = chunk.start();
                            System.out.println();
                        })
                        .onContentBlockDelta(chunk -> {
                            String responseText;
                            if(chunk.delta().text() != null) {
                                responseText = chunk.delta().text();
                            } else {
                                responseText = chunk.delta().toolUse().input();
                            }
                            System.out.print(responseText);
                            sb.append(responseText);
                        })
                        .onMessageStop(event -> System.out.print(sb))
                        .onMetadata(data -> {
                            System.out.println(data.usage().totalTokens());
                        })
                        .build())
                .onError(err -> System.err.printf("Can't invoke '%s': %s", modelId, err.getMessage()))
                .build();
        // Create the input text and embed it in a message object with the user
        // role.
        // String inputText = "描述一下这个图片";
        String base64String = "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"; // 示例base64字符串
        byte[] decodedBytes = Base64.getDecoder().decode(base64String);
        // ContentBlock contentBlock = ContentBlock.builder()
        // .image(ImageBlock.builder()
        // .format("png")
        // .source(ImageSource.builder()
        // .bytes(SdkBytes.fromByteArray(decodedBytes))
        // .build())
        // .build())
        // .build();
        software.amazon.awssdk.services.bedrockruntime.model.ToolSpecification.Builder toolBuilder = software.amazon.awssdk.services.bedrockruntime.model.ToolSpecification
                .builder();
        toolBuilder.name("queryWeather");
        toolBuilder.description("queryWeather");
        toolBuilder.inputSchema(ToolInputSchema.builder().json(convertObjectToDocument(schemaMap)).build());
        Tool tool = Tool.fromToolSpec(toolBuilder.build());
        String inputText = "查一下，北纬60度东经110度，今天的天气";
        ContentBlock contentBlock = ContentBlock.builder()
                .text(inputText).build();
        Message message = Message.builder()
                .content(contentBlock)
                .role(ConversationRole.USER)
                .build();
        ConverseStreamRequest request = ConverseStreamRequest.builder().modelId(modelId).messages(message)
                .toolConfig(ToolConfiguration.builder().tools(tool).build())
                .inferenceConfig(InferenceConfiguration.builder().maxTokens(512).temperature(0.5F).topP(0.9F).build())
                .build();
        try {
            client.converseStream(request, responseStreamHandler).get();
        } catch (ExecutionException | InterruptedException e) {
            System.out.printf("ERROR: Can't invoke '%s'. Reason: %s%n", modelId, e.getMessage());
            throw new RuntimeException(e);
        }
    }

    @Data
    class NativeRequest {
        private String anthropic_version;
        private int max_tokens_to_sample;
        private double temperature;
        private String prompt;
    }

    @SuppressWarnings("unchecked")
    public static Document convertObjectToDocument(Object value) {
        if(value == null) {
            return Document.fromNull();
        } else if(value instanceof String) {
            return Document.fromString((String) value);
        } else if(value instanceof Boolean) {
            return Document.fromBoolean((Boolean) value);
        } else if(value instanceof Integer) {
            return Document.fromNumber((Integer) value);
        } else if(value instanceof Long) {
            return Document.fromNumber((Long) value);
        } else if(value instanceof Float) {
            return Document.fromNumber((Float) value);
        } else if(value instanceof Double) {
            return Document.fromNumber((Double) value);
        } else if(value instanceof BigDecimal) {
            return Document.fromNumber((BigDecimal) value);
        } else if(value instanceof BigInteger) {
            return Document.fromNumber((BigInteger) value);
        } else if(value instanceof List) {
            List listValue = (List) value;
            return Document.fromList((List<Document>) listValue.stream().map(AwsChannel::convertObjectToDocument).collect(Collectors.toList()));
        } else if(value instanceof Map) {
            return convertMapToDocument((Map<String, Object>) value);
        } else {
            throw new IllegalArgumentException("Unsupported value type:" + value.getClass().getSimpleName());
        }
    }

    private static Document convertMapToDocument(Map<String, Object> value) {
        Map<String, Document> attr = value.entrySet().stream()
                .collect(Collectors.toMap(e -> e.getKey(), e -> convertObjectToDocument(e.getValue())));
        return Document.fromMap(attr);
    }

}
