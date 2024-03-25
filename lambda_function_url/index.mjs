// import { promisify } from 'util';
// import { Readable,pipeline } from 'stream';
// // const pipelinePromise = promisify(pipeline);

import  {
    BedrockRuntimeClient,
    InvokeModelWithResponseStreamCommand,
  }  from "@aws-sdk/client-bedrock-runtime";
  
  // Create a BedrockRuntimeClient with your configuration
  //get region from env variable
  const region = process.env.AWS_REGION??'us-east-1';
  const client = new BedrockRuntimeClient({ region: region })


  
  
  const main_stream = async (prompt,responseStream)=>{
    const input = {
        modelId: "anthropic.claude-3-sonnet-20240229-v1:0",
        contentType: "application/json",
        accept: "application/json",
        body: JSON.stringify({
          anthropic_version: "bedrock-2023-05-31",
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content: [
                {
                  type: "text",
                  text: prompt,
                },
              ],
            },
          ],
        }),
      };
    const command = new InvokeModelWithResponseStreamCommand(input);
    const response = await client.send(command);
    // return response.body
    // console.log(response);
    let text = ''
    for await (const item of response.body) {
      if (item.chunk?.bytes) {
        const outputs = JSON.parse(Buffer.concat([item.chunk.bytes]).toString('utf-8'));
          responseStream.write(outputs)
              if (outputs.delta?.type==="text_delta") {
                text += outputs.delta?.text
                console.log(text);
              }
      }
    }
    responseStream.end()
  }


export const handler = awslambda.streamifyResponse(async (event, responseStream, _context) => {
    // As an example, convert event to a readable stream.
    await main_stream(event.prompt,responseStream);
  });