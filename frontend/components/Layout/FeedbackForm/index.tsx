import { Form, Input, Popover, Button } from 'antd';
import React from 'react';


const { TextArea } = Input;

type State = {
   visible: boolean;
};


export default class FeedbackForm extends React.Component<{}, State> {
   state: State = {
     visible: false
   };
   
   validateMessages = {
      required: '${label} is required!',
      types: {
         email: '${label} is not a valid email!',
      },
   };

   content = (
      <Form 
         onFinish={this.handleFormSuccess} 
         onFinishFailed={this.handleFormFailed} 
         validateMessages={this.validateMessages} 
         layout="vertical"
         // className="popover-form"
      >
         <Form.Item required name="email" label="Email" rules={[{ required: true }]}>
            <Input placeholder="Your email address" type="email" />
         </Form.Item>
         <Form.Item required name="feedback" label="Feedback" rules={[{ required: true }]}>
            <TextArea rows={4} cols={25} maxLength={500} placeholder="Your feedback..." />
         </Form.Item>
         <Form.Item>
            <div className="flex justify-between">
               <Button type='primary' htmlType='submit'>Send</Button>
               <Button danger type="text" onClick={(event) => this.setState({ visible: false })}>
                  Cancel
               </Button>
            </div>
         </Form.Item>
      </Form>
   );

   constructor(props: {}) {
      super(props);
      this.handleFormSuccess = this.handleFormSuccess.bind(this);
      this.handleFormFailed = this.handleFormFailed.bind(this);
      this.handleVisibleChange = this.handleVisibleChange.bind(this);
   }

   handleVisibleChange(visible: boolean) {
      this.setState({ visible });
   }

   handleFormSuccess(values: any) {
      // console.log(values);
      this.setState({ visible: false });
   }

   handleFormFailed({ values, errorFields, outOfDate }: any) {
      // console.log(values);
      // console.log(errorFields);
      // console.log(outOfDate);
   }

   render() {
      return (
         <Popover 
            content={this.content} 
            placement="right"
            trigger="click" 
            className="popover"
            visible={this.state.visible}
            onVisibleChange={this.handleVisibleChange}
            title={
               <p className="text-center pt-5">
                  Share any feedback about our services
               </p>
            }
         >
            <Button>Feedback</Button>
         </Popover>
      );
   }
   
}

