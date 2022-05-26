import { MdDoNotDisturbAlt } from "react-icons/md";
import { GiCheckMark } from "react-icons/gi";
import { Tooltip, Table } from "antd";
import { getCtaBtn } from "../../../utils";
import type { UserPlanState } from '../../../types';
import type { ColumnsType } from 'antd/es/table';


type Props = {
   planState: UserPlanState
}

type PlanInfo = {
   key: number;
   topic: React.ReactNode;
   free: React.ReactNode;
   premium: React.ReactNode;
   gold: React.ReactNode;
}


const PricingTable: React.FunctionComponent<Props> = (props) => {
   const { planState } = props;
   

   
   // See https://ant.design/components/table/#Using-in-TypeScript/
   const columns: ColumnsType<PlanInfo> = [
      {
         title: "",
         dataIndex: "topic"
         // className: "topicColumn",
         // render: (content: React.ReactNode) => {
         //   return (
         //     <div className="renderedCol">{content}</div>
         //   );
         // },
      },
      {
         title: <h3 className="font-bold text-lg">Free</h3>,
         dataIndex: "free",
         align: "center"
      },
      {
         title: (
            <h3 className="font-bold text-lg" style={{ color: "var(--blue)" }}>
               Premium
            </h3>
         ),
         dataIndex: "premium",
         align: "center"
      },
      {
         title: (
            <h3 className="font-bold text-lg" style={{ color: "gold" }}>
               Gold
            </h3>
         ),
         dataIndex: "gold",
         align: "center"
      }
   ];

   const data: PlanInfo[] = [
      {
         key: 0,
         topic: "Ad-free service",
         free: <MdDoNotDisturbAlt className="inline-block" />,
         premium: <GiCheckMark className="inline-block" />,
         gold: <GiCheckMark className="inline-block" />
      },
      {
         key: 1,
         topic: (
            <Tooltip placement="top" title="2FA description">
               <div className="tooltipDiv">2FA Authentication</div>
            </Tooltip>
         ),
         free: <MdDoNotDisturbAlt className="inline-block" />,
         premium: <MdDoNotDisturbAlt className="inline-block" />,
         gold: <GiCheckMark className="inline-block" />
      },
      {
         key: 2,
         topic: (
            <Tooltip placement="top" title="Active sessions description">
               <div className="tooltipDiv">Active Sessions</div>
            </Tooltip>
         ),
         free: "1",
         premium: "2",
         gold: "5"
      },
      {
         key: 3,
         topic: (
            <Tooltip placement="top" title="Description">
               <div className="tooltipDiv">Max devices per session</div>
            </Tooltip>
         ),
         free: "2",
         premium: "4",
         gold: "Unlimited"
      },
      {
         key: 4,
         topic: (
            <Tooltip placement="top" title="Description">
               <div className="tooltipDiv">Max file size per transaction</div>
            </Tooltip>
         ),
         free: (
            <span>
               100mb | &nbsp;
               <span className="text-sm">file link expires after 24hrs</span>
            </span>
         ),
         premium: (
            <span>
               500mb | &nbsp;
               <span className="text-sm">file link expires after 24hrs</span>
            </span>
         ),
         gold: (
            <span>
               1gb | &nbsp;
               <span className="text-sm">file link expires after 1week</span>
            </span>
         )
      },
      {
         key: 5,
         topic: (
            <Tooltip placement="top" title="Description">
               <div className="tooltipDiv">Max file size per day</div>
            </Tooltip>
         ),
         free: "1GB",
         premium: "4GB",
         gold: "10GB"
      },
      {
         key: 6,
         topic: "",
         free: getCtaBtn("free", planState, true),
         premium: getCtaBtn("premium", planState, true),
         gold: getCtaBtn("gold", planState, true)
      }
   ];


   return (
      <section className="">
         <h1 className="text-center text-2xl mt-8 mb-5">Compare plan features</h1>
         <Table<PlanInfo>
            bordered
            scroll={{ x: 700 }}
            pagination={false}
            columns={columns}
            dataSource={data}
         // footer={(data) => 'Footer'}
         />
         
         <style jsx global>{`
            .tooltipDiv {
               border-bottom: 1px dotted gray;
               /* Prevent border from extending content */
               width: fit-content;
            }
         `}</style>
      </section>
   );
};

export default PricingTable;
